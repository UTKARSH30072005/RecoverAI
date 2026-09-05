\# 🤖 RecoverAI — AI-Powered Revenue Recovery System



> \*\*Turn failed payments into recovered revenue using AI-driven prediction, decision-making, and automated recovery actions.\*\*



RecoverAI is an AI-powered revenue recovery system designed to intelligently handle failed payment events. Instead of treating every failed transaction equally, RecoverAI analyzes transaction and customer-related signals, predicts the probability of successful recovery, and recommends the most suitable recovery action.



The system combines \*\*Machine Learning + Decision Engine + Real-Time Processing + Payment Gateway Integration + Audit Logging\*\* into a single workflow.



\---



\## 🚀 Key Features



\* 🔮 \*\*Recovery Prediction\*\* — Predicts the probability that a failed payment can be recovered.

\* 🧠 \*\*AI Decision Engine\*\* — Selects an appropriate recovery strategy based on prediction and transaction context.

\* ⚡ \*\*Real-Time Processing\*\* — Processes incoming payment events and generates recovery recommendations.

\* 💳 \*\*Payment Gateway Integration\*\* — Designed to work with Razorpay payment workflows.

\* 🔗 \*\*Recovery Link Generation\*\* — Generates a recovery action/link for eligible transactions.

\* 📊 \*\*Revenue Intelligence\*\* — Estimates expected recoverable revenue.

\* 📝 \*\*Audit Logging\*\* — Records recovery decisions and execution results.

\* 🔐 \*\*Secure Credentials\*\* — API credentials are loaded through environment variables.

\* 🎯 \*\*Priority-Based Recovery\*\* — Transactions can be classified into different risk/priority levels.



\---



\## 🏗️ System Architecture



```text

&#x20;                   ┌──────────────────────┐

&#x20;                   │   Payment Event      │

&#x20;                   │   Failed Transaction │

&#x20;                   └──────────┬───────────┘

&#x20;                              │

&#x20;                              ▼

&#x20;                   ┌──────────────────────┐

&#x20;                   │ Real-Time Event      │

&#x20;                   │ Processor            │

&#x20;                   └──────────┬───────────┘

&#x20;                              │

&#x20;                              ▼

&#x20;                   ┌──────────────────────┐

&#x20;                   │ Feature Processing   │

&#x20;                   │ \& Preprocessing      │

&#x20;                   └──────────┬───────────┘

&#x20;                              │

&#x20;                              ▼

&#x20;                   ┌──────────────────────┐

&#x20;                   │ ML Recovery Model    │

&#x20;                   │ Recovery Probability │

&#x20;                   └──────────┬───────────┘

&#x20;                              │

&#x20;                              ▼

&#x20;                   ┌──────────────────────┐

&#x20;                   │ Decision Engine      │

&#x20;                   │                     │

&#x20;                   │ Action + Priority   │

&#x20;                   └──────────┬───────────┘

&#x20;                              │

&#x20;                              ▼

&#x20;                   ┌──────────────────────┐

&#x20;                   │ Recovery Agent       │

&#x20;                   │ / Action Executor   │

&#x20;                   └──────────┬───────────┘

&#x20;                              │

&#x20;                   ┌──────────┴───────────┐

&#x20;                   ▼                      ▼

&#x20;           ┌──────────────┐       ┌──────────────┐

&#x20;           │ Payment      │       │ Audit Log    │

&#x20;           │ Recovery     │       │              │

&#x20;           └──────────────┘       └──────────────┘

```



\---



\## 📁 Project Structure



```text

RecoverAI/

│

├── agent/

│   ├── action\_executor.py

│   ├── audit\_logger.py

│   ├── decision\_engine.py

│   ├── live\_processor.py

│   ├── live\_recovery\_agent.py

│   └── recovery\_agent.py

│

├── data/

│   ├── explore\_dataset.py

│   └── generate\_dataset.py

│

├── ml/

│   ├── predict.py

│   └── train\_model.py

│

├── app.py

├── live\_recovery\_agent.py

├── payment\_gateway.py

├── realtime\_engine.py

├── .env.example

├── .gitignore

└── README.md

```



\---



\## 🧠 Machine Learning Pipeline



RecoverAI uses a supervised machine-learning pipeline to estimate recovery probability.



\### Pipeline



```text

Transaction Data

&#x20;      │

&#x20;      ▼

Data Preparation

&#x20;      │

&#x20;      ▼

Feature Engineering

&#x20;      │

&#x20;      ▼

Train/Test Split

&#x20;      │

&#x20;      ▼

Preprocessing

&#x20;      │

&#x20;      ▼

XGBoost Model

&#x20;      │

&#x20;      ▼

Recovery Probability

&#x20;      │

&#x20;      ▼

Decision Engine

```



The model is designed so that prediction features represent information available around the payment-failure event, helping avoid \*\*data leakage\*\* from future recovery outcomes.



\### Model Performance



Current experimental model results:



| Metric    |  Score |

| --------- | -----: |

| Accuracy  | 65.15% |

| Precision | 66.89% |

| Recall    | 91.18% |

| F1 Score  | 77.17% |

| ROC-AUC   | 58.28% |



> \*\*Note:\*\* These metrics are from the current development dataset/model and should not be interpreted as production performance.



\---



\## 💡 Example Prediction



Example transaction:



```text

Transaction Amount: ₹2,500



Recovery Probability: 57.74%



Expected Recovery: ₹1,443.45



Risk Level: MEDIUM



Recommended Action:

ALTERNATE\_PAYMENT



Priority:

MEDIUM

```



The expected recovery value can be estimated using:



```text

Expected Recovery

= Transaction Amount × Recovery Probability

```



\---



\## ⚙️ Decision Engine



The Decision Engine converts the ML prediction into an actionable recovery strategy.



Example:



```text

ML Prediction

&#x20;    │

&#x20;    ▼

Recovery Probability

&#x20;    │

&#x20;    ▼

Risk / Priority Assessment

&#x20;    │

&#x20;    ▼

Recommended Action

```



Possible recovery actions can include:



\* Alternate payment method

\* Recovery link

\* Retry payment

\* Customer notification

\* Deferred retry

\* No immediate action



The final action can be extended according to business rules and payment context.



\---



\## ⚡ Real-Time Recovery Flow



RecoverAI is designed around event-driven processing:



```text

Payment Failure

&#x20;     ↓

Event Received

&#x20;     ↓

Transaction Features Extracted

&#x20;     ↓

ML Prediction

&#x20;     ↓

Decision Engine

&#x20;     ↓

Recovery Action

&#x20;     ↓

Payment/Recovery Link

&#x20;     ↓

Audit Log

```



This allows the system to respond to payment failures immediately rather than relying only on batch analysis.



\---



\## 💳 Payment Gateway Integration



RecoverAI includes a payment gateway integration layer.



Credentials are loaded from environment variables:



```python

RAZORPAY\_KEY\_ID = os.getenv("RAZORPAY\_KEY\_ID")

RAZORPAY\_KEY\_SECRET = os.getenv("RAZORPAY\_KEY\_SECRET")

```



\*\*Never commit API credentials to GitHub.\*\*



\---



\## 🔐 Environment Setup



Create a `.env` file in the project root:



```env

RAZORPAY\_KEY\_ID=your\_razorpay\_key\_id

RAZORPAY\_KEY\_SECRET=your\_razorpay\_key\_secret

```



The `.env` file is intentionally excluded from Git using `.gitignore`.



\---



\## 🛠️ Installation



\### 1. Clone the repository



```bash

git clone https://github.com/UTKARSH30072005/RecoverAI.git

cd RecoverAI

```



\### 2. Create a virtual environment



Windows:



```powershell

python -m venv venv

```



Activate it:



```powershell

venv\\Scripts\\activate

```



\### 3. Install dependencies



If a `requirements.txt` file is present:



```powershell

pip install -r requirements.txt

```



Otherwise install the required project packages according to the imports used by the application.



\### 4. Configure environment variables



Create `.env`:



```env

RAZORPAY\_KEY\_ID=your\_razorpay\_key\_id

RAZORPAY\_KEY\_SECRET=your\_razorpay\_key\_secret

```



\---



\## ▶️ Run the Application



Start the Streamlit dashboard:



```powershell

streamlit run app.py

```



The application will open in your browser.



\---



\## 🧪 Model Training



To train the recovery prediction model:



```powershell

python ml/train\_model.py

```



The training pipeline prepares the data and trains the machine-learning model.



\---



\## 📊 Dataset



The development version of RecoverAI uses a generated transaction dataset for experimentation and demonstration.



The dataset contains transaction-level information such as:



\* Transaction amount

\* Payment method

\* Customer attributes

\* Transaction context

\* Failure information

\* Recovery-related features



Generated CSV files are intentionally excluded from the Git repository to keep the repository clean and avoid committing generated artifacts.



\---



\## 🔒 Security



Sensitive credentials are never stored directly in source code.



The repository uses:



```text

.env

```



for local secrets and:



```text

.env.example

```



for documenting required environment variables.



Generated datasets, audit logs, and trained model binaries are also excluded from Git.



\---



\## 🎯 Business Value



RecoverAI focuses on a simple business problem:



> \*\*When a payment fails, what should happen next to maximize the probability of recovering the lost revenue?\*\*



Instead of applying the same retry strategy to every failed payment, RecoverAI attempts to make the recovery process:



\* More intelligent

\* More targeted

\* More automated

\* More measurable

\* More scalable



\---



\## 🔮 Future Improvements



\* Real production payment webhook integration

\* More robust feature engineering

\* Model calibration and threshold optimization

\* A/B testing of recovery strategies

\* Customer segmentation

\* Reinforcement-learning-based action selection

\* Automated notification channels

\* Revenue recovery analytics

\* Model monitoring and drift detection

\* Production database integration

\* Cloud deployment

\* Authentication and role-based access

\* Improved observability and monitoring



\---



\## 🧰 Technology Stack



| Technology    | Purpose                     |

| ------------- | --------------------------- |

| Python        | Core development            |

| XGBoost       | Recovery prediction         |

| Scikit-learn  | ML preprocessing/evaluation |

| Pandas        | Data processing             |

| Streamlit     | Dashboard                   |

| Razorpay      | Payment gateway integration |

| Git/GitHub    | Version control             |

| Python-dotenv | Environment configuration   |



\---



\## 👨‍💻 Author



\*\*Utkarsh Patil\*\*



Electronics \& Computer Engineering

Data Science



GitHub:

https://github.com/UTKARSH30072005



\---



\## 📌 Project Status



\*\*Status:\*\* 🚧 Prototype / Hackathon Project



RecoverAI is currently designed as an experimental AI-powered revenue recovery platform. Production deployment would require additional security, monitoring, model validation, payment-gateway configuration, and infrastructure hardening.



