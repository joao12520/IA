#	Bank Account Fraud Detection

## General Notes
- Biased, each dataset has distinct controlled types of bias;
- Imbalanced, this setting presents an **extremely low prevalence of positive class**;
- Laplacian noise was added to the data before the generative process;
- Each dataset has:
	- 1M instances;
	- 30 realistic features used in the fraud detection use-case;
	- Temporal information (month);
	- Protected attributes (age group, employment status and % income);

## Dataset Variants

![](https://www.googleapis.com/download/storage/v1/b/kaggle-user-content/o/inbox%2F3349776%2F4271ec763b04362801df2660c6e2ec30%2FScreenshot%20from%202022-11-29%2017-42-41.png?generation=1669743799938811&alt=media)

## Evaluation Metrics

### Performance 

- Accuracy is **NOT** an adequate evaluation metric, as the dataset is highly imbalanced (with only approximately 1% of the transactions labeled as fraudulent).
- The performance evaluation will be based on the AUC-ROC, and the model's thresholds must guarantee an FPR value of 5% or lower.

### Fairness
- False positives mean denied bank accounts for legitimate applicants. Having one group of people be constantly denied would have negative societal impacts for the company.
- False negatives mean an accepted bank account for a malicious applicant, which incurs in loses for the company.
- A high FPR would mean discrimination against a certain group of people, and the societal impact would cause the company's reputation to be damage, which would lead to serious losses. As such, the **FPR difference across protected groups must be minimized**, and the threshold values for the model must guarantee an **FPR value of AT MOST 5%**.

## Dataset analysis

### Columns

- **fraud_bool**: Fraud label (1 if fraud, 0 if legit)

- **income**: Annual income of the applicant in quantiles. Ranges between [0, 1].

- **name_email_similarity**: Metric of similarity between email and applicant’s name. Higher values represent higher similarity. Ranges between [0, 1].

- **prev_address_months_count**: Number of months in previous registered address of the applicant, i.e. the applicant’s previous residence, if applicable. Ranges between [−1, 380] months (-1 is a missing value).

- **current_address_months_count**: Months in currently registered address of the applicant. Ranges between [−1, 406] months (-1 is a missing value).

- **customer_age**: Applicant’s age in bins per decade (e.g, 20-29 is represented as 20).

- **days_since_request**: Number of days passed since application was done. Ranges between [0, 78] days.

- **intended_balcon_amount**: Initial transferred amount for application. Ranges between [−1, 108].

- **payment_type**: Credit payment plan type. 5 possible (annonymized) values.

- **zip_count_4w**: Number of applications within same zip code in last 4 weeks. Ranges between [1, 5767].

- **velocity_6h**: Velocity of total applications made in last 6 hours i.e., average number of applications per hour in the last 6 hours. Ranges between [−211, 24763].

- **velocity_24h**: Velocity of total applications made in last 24 hours i.e., average number of applications per hour in the last 24 hours. Ranges between [1329, 9527].

- **velocity_4w**: Velocity of total applications made in last 4 weeks, i.e., average number of applications per hour in the last 4 weeks. Ranges between [2779, 7043].

- **bank_branch_count_8w**: Number of total applications in the selected bank branch in last 8 weeks. Ranges between [0, 2521].

- **date_of_birth_distinct_emails_4w**: Number of emails for applicants with same date of birth in last 4 weeks. Ranges between [0, 42].

- **employment_status**: Employment status of the applicant. 7 possible (annonymized) values.

- **credit_risk_score**: Internal score of application risk. Ranges between [−176, 387].

- **email_is_free**: Domain of application email (either free or paid).

- **housing_status**: Current residential status for applicant. 7 possible (annonymized) values.

- **phone_home_valid**: Validity of provided home phone.

- **phone_mobile_valid**: Validity of provided mobile phone.

- **bank_months_count**: How old is previous account (if held) in months. Ranges between [−1, 31] months (-1 is a missing value).

- **has_other_cards**: If applicant has other cards from the same banking company.

- **proposed_credit_limit**: Applicant’s proposed credit limit. Ranges between [200, 2000].

- **foreign_request**: If origin country of request is different from bank’s country.

- **source**: Online source of application. Either browser(INTERNET) or mobile app (APP).

- **session_length_in_minutes**: Length of user session in banking website in minutes. Ranges between [−1, 107] minutes

- **device_os**: Operative system of device that made request. Possible values are: Windows, Macintox, Linux, X11, or other.

- **keep_alive_session**: User option on session logout

- **device_distinct_emails_8w**: Number of distinct emails in banking website from the used device in last 8 weeks. Ranges between [0, 3].

- **device_fraud_count**: Number of fraudulent applications with used device. Ranges between [0, 1].

- **month**: Month where the application was made. Ranges between [0, 7].
