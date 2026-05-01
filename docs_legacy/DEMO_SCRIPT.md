# Demo Script - 5-7 Minute Walkthrough

## Setup (Before Demo)

**Pre-demo checklist:**
- [ ] Flask app running (localhost:5000)
- [ ] Dashboard running (localhost:8501)
- [ ] Database cleared (fresh start)
- [ ] All defenses OFF in config.py
- [ ] Browser tabs ready (Flask login, Dashboard)
- [ ] Terminal ready for attack script

---

## Demo Flow (7 minutes)

### Part 1: Introduction (1 minute)

**Script:**
> "Today I'm presenting our Login Security Testbed - a controlled environment for testing authentication attacks and defenses. This project demonstrates common vulnerabilities in login systems and how to defend against them."

**Show:**
- Project folder structure
- Mention: 4 attack types, 8 defense mechanisms, real-time monitoring

---

### Part 2: The Vulnerable System (1.5 minutes)

**Script:**
> "First, let me show you our intentionally vulnerable login system. It uses MD5 hashing - which is cryptographically broken - and has no defenses enabled by default."

**Demo:**
1. Open browser: http://localhost:5000
2. Show login page
3. Try login: `admin` / `wrongpassword` → Fails
4. Try login: `admin` / `admin123` → Success
5. Show dashboard page
6. Logout

**Point out:**
- Generic error messages (no username enumeration)
- But still vulnerable to brute force

---

### Part 3: Attack Demonstration (2 minutes)

**Script:**
> "Now let's simulate a brute-force attack. This script will systematically try passwords from a wordlist until it finds the correct one."

**Demo:**
1. Switch to dashboard tab (http://localhost:8501)
2. Show: "No attempts yet" or clear dashboard
3. Run attack: `test_bruteforce.bat`
4. Type "yes" to confirm
5. **Watch dashboard update in real-time:**
   - Attempts counter increasing
   - Live feed showing each attempt
   - Charts updating
   - IP activity

**Script while attack runs:**
> "Notice how the dashboard shows every attempt in real-time. The attack is trying hundreds of passwords per minute. Without any defenses, this is extremely fast."

6. Wait for success message
7. Show: Password found in X attempts, Y seconds

**Point out:**
- Attack succeeded easily
- No rate limiting
- No account lockout
- System is completely vulnerable

---

### Part 4: Defense Mechanisms (1.5 minutes)

**Script:**
> "Now let's enable defenses. I'll activate rate limiting, which restricts login attempts per minute."

**Demo:**
1. Open `config.py` in editor
2. Show current config (all False)
3. Change: `RATE_LIMIT_ENABLED = True`
4. Save file
5. Restart Flask app (Ctrl+C, then run again)
6. Show dashboard - defense status now shows "Rate Limiting: ON"

**Script:**
> "Let's run the same attack again."

7. Clear database: `manage_database.bat` → Option 2
8. Run attack again: `test_bruteforce.bat`
9. **Watch dashboard:**
   - Attack starts
   - Gets blocked quickly (after ~10 attempts)
   - "Blocked" counter increases
   - Attack fails

**Script:**
> "Notice the attack was blocked after just 10 attempts. Rate limiting drastically reduces the attack speed, making brute force impractical."

---

### Part 5: Combined Defenses (1 minute)

**Script:**
> "In production, you'd use multiple defenses together. Let me enable all defenses at once."

**Demo:**
1. Open `config.py`
2. Set ALL defenses to True
3. Restart Flask app
4. Show dashboard - all defenses ON
5. Run attack: `test_bruteforce.bat`
6. **Watch:**
   - Attack blocked almost immediately
   - Multiple defense mechanisms triggering
   - Very low success rate

**Script:**
> "With all defenses active, the attack is stopped almost instantly. This demonstrates the principle of defense-in-depth - multiple layers of security."

---

### Part 6: Conclusion & Results (30 seconds)

**Script:**
> "Our experiments show that:
> - Without defenses: attacks succeed in seconds
> - With rate limiting: attack speed reduced by 90%
> - With all defenses: near-zero success rate
>
> Key takeaway: Never rely on a single defense. Use multiple layers - rate limiting, account lockout, CAPTCHA, and MFA together."

**Show:**
- Dashboard with final statistics
- Mention: Full report with detailed metrics available

---

## Backup Demos (If Time Permits)

### Credential Stuffing Demo
1. Run: `test_credential_stuffing.bat`
2. Show: Multiple accounts compromised
3. Explain: Uses leaked username:password pairs

### Distributed Attack Demo
1. Show: IP rotation in code
2. Run distributed attack
3. Show: Different IPs in dashboard
4. Explain: Bypasses IP-based defenses

---

## Q&A Preparation

**Expected Questions:**

**Q: "Is this safe to use on real systems?"**
A: "No, this is for educational purposes only. It contains intentional vulnerabilities. Never deploy this to production."

**Q: "What's the most effective defense?"**
A: "Rate limiting combined with account lockout. But the best approach is using all defenses together."

**Q: "Can these attacks be detected?"**
A: "Yes, our anomaly detection flags suspicious patterns. In production, you'd integrate with SIEM systems for alerting."

**Q: "What about distributed attacks?"**
A: "IP rotation can bypass simple IP blocking. That's why we need multiple defenses - CAPTCHA, device fingerprinting, behavioral analysis."

**Q: "How long did this project take?"**
A: "Approximately [X weeks/months], including research, implementation, testing, and documentation."

---

## Technical Difficulties Backup

**If Flask won't start:**
- Show code walkthrough instead
- Explain architecture with diagrams
- Show pre-recorded screenshots

**If attack script fails:**
- Manually demonstrate login attempts
- Show logged attempts in database
- Explain expected behavior

**If dashboard won't load:**
- Show database directly with `db_utils.py stats`
- Show result JSON files
- Explain metrics verbally

---

## Closing Statement

> "This project demonstrates the importance of authentication security. Real-world systems face these attacks daily. By understanding both the attack and defense sides, we can build more secure applications. Thank you!"

---

## Demo Checklist

**Before starting:**
- [ ] All applications running
- [ ] Database cleared
- [ ] Config set to baseline (all OFF)
- [ ] Browser tabs open
- [ ] Terminal ready
- [ ] Backup slides ready

**After demo:**
- [ ] Stop all applications
- [ ] Save any generated data
- [ ] Prepare for Q&A
