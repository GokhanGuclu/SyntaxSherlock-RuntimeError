import pandas as pd
import joblib
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, roc_auc_score

DATASET_PATH = "dataset_thinking.csv"
MODEL_PATH = "syntax_sherlock_model.pkl"

# =====================================================
# VERİYİ YÜKLE
# =====================================================

df = pd.read_csv(DATASET_PATH)

# -----------------------------------------------------
# MODEL–SCANNER FEATURE SÖZLEŞMESİ
# -----------------------------------------------------
FEATURES = [
    "is_division",
    "is_index",
    "inside_loop_depth",
    "if_depth",
    "try_depth",
    "complexity_score",
    "variable_entropy"
]

TARGET = "runtime_error"

# =====================================================
# FEATURE / LABEL AYRIMI
# =====================================================

X = df[FEATURES]
y = df[TARGET]

# =====================================================
# TRAIN / TEST SPLIT
# =====================================================

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42,
    stratify=y
)

# =====================================================
# MODEL
# =====================================================

model = RandomForestClassifier(
    n_estimators=150,
    max_depth=10,          # bilinçli sınırlı
    min_samples_leaf=10,   # ezberi engeller
    class_weight="balanced",
    random_state=42,
    n_jobs=-1
)

# =====================================================
# TRAIN
# =====================================================

model.fit(X_train, y_train)

# =====================================================
# DEĞERLENDİRME
# =====================================================

probs = model.predict_proba(X_test)[:, 1]
auc = roc_auc_score(y_test, probs)

print(f"\n🎯 ROC-AUC: {auc:.3f}\n")

y_pred = model.predict(X_test)
print(classification_report(y_test, y_pred))

# =====================================================
# FEATURE SÖZLEŞMESİ DOĞRULAMA
# =====================================================

print("📌 Model feature listesi:")
print(list(model.feature_names_in_))

# =====================================================
# MODELİ KAYDET
# =====================================================

joblib.dump(model, MODEL_PATH)
print(f"\n✅ Model kaydedildi: {MODEL_PATH}")
asdasda
