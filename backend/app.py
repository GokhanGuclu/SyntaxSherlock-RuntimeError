import sys
import os
from scanner import load_model, analyze_code

# =============================================================================
# SyntaxSherlock CLI (backend/app.py)
# =============================================================================

MODEL_PATH = os.path.join(os.path.dirname(__file__), "syntax_sherlock_model.pkl")

def main():
    if len(sys.argv) < 2:
        print("Kullanım: python app.py dosya.py")
        sys.exit(1)
    
    path = sys.argv[1]
    if not os.path.exists(path):
        print(f"❌ Dosya bulunamadı: {path}")
        sys.exit(1)

    # Modeli Yükle
    try:
        model = load_model(MODEL_PATH)
    except FileNotFoundError:
        print(f"❌ {MODEL_PATH} bulunamadı. Lütfen önce 'python train.py' çalıştırın.")
        sys.exit(1)

    print(f"🔍 Taranıyor: {path}")
    
    with open(path, "r", encoding="utf-8") as f:
        source = f.read()
    
    results = analyze_code(source, model)
    
    if not results:
        print("✅ Riskli işlem bulunamadı.")
        return
        
    if "error" in results[0]:
        print(f"❌ Syntax Hatası (Satır {results[0]['lineno']}): {results[0]['error']}")
        return

    print("\n🔍 SyntaxSherlock Analiz Sonuçları")
    print("=" * 80)
    print(f"{'SATIR':<8} {'RİSK':<8} {'TÜR':<12} {'KOD':<35} {'DETAY'}")
    print("-" * 80)
    
    # TÜM SONUÇLARI GÖSTER (Güvenli olanlar dahil)
    for r in results:
        risk = r["risk_score"]
        
        # Renk kodu belirleme
        if risk >= 0.8: 
            color_code = "🔴"
            status = "KRİTİK"
        elif risk >= 0.5: 
            color_code = "🟠"
            status = "ŞÜPHELİ"
        else: 
            color_code = "🟢"
            status = "GÜVENLİ"
        
        # Kod snippet'ini kısalt
        expr_short = r["code"]
        if len(expr_short) > 32:
            expr_short = expr_short[:29] + "..."
        
        # Detay mesajı
        detail = r["message"] if r["message"] else status
            
        print(f"{r['lineno']:<8} %{risk*100:<7.1f} {r['type']:<12} {expr_short:<35} {color_code} {detail}")

    print("=" * 80)

if __name__ == "__main__":
    main()
