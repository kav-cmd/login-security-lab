# Experiment Results Template

## Experiment Metadata

**Date:** _________________
**Conducted By:** _________________
**Environment:** Local testbed (localhost:5000)

---

## Scenario 1: Baseline (No Defenses)

### Configuration
```python
RATE_LIMIT_ENABLED = False
ACCOUNT_LOCKOUT = False
IP_BLOCKING = False
CAPTCHA_ENABLED = False
ANOMALY_DETECTION = False
```

### Attack 1: Brute Force
- **Target:** admin
- **Wordlist:** passwords.txt (500 passwords)
- **Start Time:** __________
- **End Time:** __________
- **Duration:** __________ seconds
- **Total Attempts:** __________
- **Successful:** __________
- **Blocked:** __________
- **Success Rate:** __________%
- **Password Found:** __________
- **Attempts to Crack:** __________

### Attack 2: Credential Stuffing
- **Credentials File:** credentials.txt (200 pairs)
- **Duration:** __________ seconds
- **Total Attempts:** __________
- **Accounts Compromised:** __________
- **Success Rate:** __________%
- **Compromised Accounts List:**
  - __________
  - __________
  - __________

### Attack 3: Distributed Attack
- **IP Pool Size:** 50
- **Duration:** __________ seconds
- **Total Attempts:** __________
- **Successful:** __________
- **Blocked:** __________

### Observations:
_________________________________________________________________
_________________________________________________________________
_________________________________________________________________

---

## Scenario 2: Rate Limiting Only

### Configuration
```python
RATE_LIMIT_ENABLED = True  # 10 requests/minute
ACCOUNT_LOCKOUT = False
IP_BLOCKING = False
CAPTCHA_ENABLED = False
ANOMALY_DETECTION = False
```

### Attack 1: Brute Force
- **Duration:** __________ seconds
- **Total Attempts:** __________
- **Successful:** __________
- **Blocked:** __________
- **Success Rate:** __________%
- **Time to Block:** __________ seconds

### Observations:
_________________________________________________________________
_________________________________________________________________

---

## Scenario 3: Account Lockout Only

### Configuration
```python
RATE_LIMIT_ENABLED = False
ACCOUNT_LOCKOUT = True  # 5 attempts, 15 min lockout
IP_BLOCKING = False
CAPTCHA_ENABLED = False
ANOMALY_DETECTION = False
```

### Attack 1: Brute Force
- **Duration:** __________ seconds
- **Total Attempts:** __________
- **Successful:** __________
- **Blocked:** __________
- **Attempts Before Lockout:** __________

### Observations:
_________________________________________________________________
_________________________________________________________________

---

## Scenario 4: IP Blocking Only

### Configuration
```python
RATE_LIMIT_ENABLED = False
ACCOUNT_LOCKOUT = False
IP_BLOCKING = True  # 50 failed attempts
CAPTCHA_ENABLED = False
ANOMALY_DETECTION = False
```

### Attack 1: Brute Force
- **Duration:** __________ seconds
- **Total Attempts:** __________
- **Successful:** __________
- **Blocked:** __________

### Attack 2: Distributed Attack
- **Duration:** __________ seconds
- **Total Attempts:** __________
- **Successful:** __________
- **Effectiveness Against IP Rotation:** __________

### Observations:
_________________________________________________________________
_________________________________________________________________

---

## Scenario 5: CAPTCHA Only

### Configuration
```python
RATE_LIMIT_ENABLED = False
ACCOUNT_LOCKOUT = False
IP_BLOCKING = False
CAPTCHA_ENABLED = True  # After 3 failed attempts
ANOMALY_DETECTION = False
```

### Attack 1: Brute Force
- **Duration:** __________ seconds
- **Total Attempts:** __________
- **Successful:** __________
- **Blocked:** __________
- **CAPTCHA Triggered After:** __________ attempts

### Observations:
_________________________________________________________________
_________________________________________________________________

---

## Scenario 6: All Defenses Combined

### Configuration
```python
RATE_LIMIT_ENABLED = True
ACCOUNT_LOCKOUT = True
IP_BLOCKING = True
CAPTCHA_ENABLED = True
ANOMALY_DETECTION = True
```

### Attack 1: Brute Force
- **Duration:** __________ seconds
- **Total Attempts:** __________
- **Successful:** __________
- **Blocked:** __________
- **Success Rate:** __________%

### Attack 2: Credential Stuffing
- **Duration:** __________ seconds
- **Total Attempts:** __________
- **Successful:** __________
- **Blocked:** __________

### Attack 3: Distributed Attack
- **Duration:** __________ seconds
- **Total Attempts:** __________
- **Successful:** __________
- **Blocked:** __________

### Observations:
_________________________________________________________________
_________________________________________________________________

---

## Scenario 7: Distributed vs All Defenses

### Configuration
All defenses ON, testing IP rotation effectiveness

### Attack: Distributed with Large IP Pool
- **IP Pool Size:** 100
- **Duration:** __________ seconds
- **Total Attempts:** __________
- **Successful:** __________
- **Blocked:** __________
- **Unique IPs Used:** __________
- **IPs Blocked:** __________

### Observations:
_________________________________________________________________
_________________________________________________________________

---

## Comparative Analysis

### Defense Effectiveness Ranking

| Defense Mechanism | Success Rate Reduction | Ease of Bypass | Overall Rating |
|-------------------|------------------------|----------------|----------------|
| Rate Limiting     | __________%            | __________     | __________     |
| Account Lockout   | __________%            | __________     | __________     |
| IP Blocking       | __________%            | __________     | __________     |
| CAPTCHA           | __________%            | __________     | __________     |
| All Combined      | __________%            | __________     | __________     |

### Key Findings

1. **Most Effective Single Defense:**
   _________________________________________________________________

2. **Least Effective Single Defense:**
   _________________________________________________________________

3. **Synergy Effect (Combined vs Individual):**
   _________________________________________________________________

4. **Distributed Attack Resilience:**
   _________________________________________________________________

5. **False Positive Rate:**
   _________________________________________________________________

### Recommendations

1. _________________________________________________________________
2. _________________________________________________________________
3. _________________________________________________________________
4. _________________________________________________________________
5. _________________________________________________________________

---

## Graphs & Charts

### To Generate:
1. Success rate comparison (bar chart)
2. Time to compromise (line chart)
3. Attempts before block (comparison)
4. Defense effectiveness matrix

### Dashboard Screenshots:
- [ ] Baseline attack
- [ ] Rate limiting in action
- [ ] Account lockout triggered
- [ ] All defenses combined
- [ ] IP activity heatmap

---

## Conclusion

### Summary:
_________________________________________________________________
_________________________________________________________________
_________________________________________________________________

### Production Recommendations:
_________________________________________________________________
_________________________________________________________________
_________________________________________________________________

### Future Work:
_________________________________________________________________
_________________________________________________________________
_________________________________________________________________

---

**Experiment Completed:** __________
**Report Prepared By:** __________
**Reviewed By:** __________
