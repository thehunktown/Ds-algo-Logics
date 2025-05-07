import streamlit as st
import requests
from datetime import datetime, timedelta

BASE_URL = "http://localhost:8000"

st.set_page_config(page_title="Referral Automation Admin", layout="wide")
st.title("🚀 Referral Automation Admin Dashboard")

tabs = st.tabs(["🧠 Jobs", "➕ Add New Job", "🏢 Companies", "📤 Referrals", "👤 Users"])

# ---------------------- Jobs Tab ----------------------
with tabs[0]:
    st.header("🧠 Job Listings")
    with st.expander("🔍 Filter Jobs"):
        jparams = {
            "role": st.text_input("Role"),
            "company_name": st.text_input("Company Name"),
            "posted_by": st.text_input("Posted By"),
            "status": st.selectbox("Status", ["", "new", "active", "closed"]),
            "critical": st.slider("Critical Level", 0, 5),
            "reminder_sent": st.selectbox("Reminder Sent", ["", "0", "1"]),
            "sort_by": st.selectbox("Sort By", ["created_at", "critical", "active_till", "role"]),
            "order": st.radio("Order", ["desc", "asc"]),
            "limit": st.slider("Page Size", 5, 50, 10)
        }
        if st.button("Apply Job Filters"):
            resp = requests.get(f"{BASE_URL}/jobs/", params=jparams)
            if resp.status_code == 200:
                jobs = resp.json()["results"]
                for job in jobs:
                    with st.expander(f"{job['role']} @ {job['company_name']}"):
                        st.write(job)
                        with st.form(f"edit_job_{job['id']}"):
                            updated = {
                                "role": st.text_input("Role", job["role"]),
                                "status": st.selectbox("Status", ["new", "active", "closed"], index=["new", "active", "closed"].index(job["status"])),
                                "critical": st.slider("Critical", 0, 5, job["critical"]),
                                "reminder_sent": st.selectbox("Reminder Sent", ["0", "1"], index=int(job["reminder_sent"]))
                            }
                            if st.form_submit_button("Update Job"):
                                requests.put(f"{BASE_URL}/jobs/{job['id']}", json=updated)
                                st.success("Updated ✅")
                        if st.button(f"Delete Job ID {job['id']}"):
                            requests.delete(f"{BASE_URL}/jobs/{job['id']}")
                            st.success("Deleted ✅")

# ---------------------- Add Job Tab ----------------------
with tabs[1]:
    st.header("➕ Add New Job")
    job_url = st.text_input("Job URL", key="add_job_url")
    company_name = st.text_input("Company Name", key="add_company_name")
    role = st.text_input("Role", key="add_job_role")
    status = st.selectbox("Status", ["new", "active", "closed"], key="add_job_status")
    job_open_date = st.date_input("Job Open Date", value=datetime.today(), key="add_job_open_date")
    posted_by = st.text_input("Posted By (optional)", key="add_posted_by")
    critical = st.slider("Critical Level", 0, 5, key="add_critical")

    # Auto-calculated fields
    reminder_date = job_open_date + timedelta(days=2)
    days_until_friday = (4 - job_open_date.weekday()) % 7
    friday_5pm = datetime.combine(
        job_open_date + timedelta(days=days_until_friday),
        datetime.strptime("17:00", "%H:%M").time()
    )

    if st.button("Submit Job", key="submit_job_btn"):
        payload = {
            "job_url": job_url,
            "company_name": company_name,
            "role": role,
            "status": status,
            "job_open_date": job_open_date.isoformat(),
            "active_till": friday_5pm.isoformat(),
            "posted_by": posted_by,
            "critical": critical,
            "reminder_date": reminder_date.isoformat(),
            "reminder_sent": 0
        }
        response = requests.post(f"{BASE_URL}/jobs/", json=payload)
        if response.status_code == 200:
            st.success("✅ Job submitted successfully!")
        else:
            st.error("❌ Failed to submit job.")

# ---------------------- Companies Tab ----------------------
with tabs[2]:
    st.header("🏢 Companies")
    with st.expander("🔍 Filter Companies"):
        cparams = {
            "name": st.text_input("Company Name Filter"),
            "domain": st.text_input("Domain Filter"),
            "email_pattern": st.text_input("Email Pattern Filter"),
            "is_verified": st.selectbox("Is Verified", ["", 0, 1])
        }
        if st.button("Filter Companies"):
            resp = requests.get(f"{BASE_URL}/companies/", params=cparams)
            if resp.status_code == 200:
                companies = resp.json()["results"]
                for c in companies:
                    with st.expander(f"{c['name']}"):
                        st.write(c)
                        with st.form(f"edit_company_{c['id']}"):
                            updated = {
                                "domain": st.text_input("Domain", c["domain"]),
                                "email_pattern": st.text_input("Email Pattern", c["email_pattern"]),
                                "is_verified": st.selectbox("Verified", [0, 1], index=c["is_verified"])
                            }
                            if st.form_submit_button("Update Company"):
                                requests.put(f"{BASE_URL}/companies/{c['id']}", json=updated)
                                st.success("Updated ✅")
                        if st.button(f"Delete Company ID {c['id']}"):
                            requests.delete(f"{BASE_URL}/companies/{c['id']}")
                            st.success("Deleted ✅")

# ---------------------- Referrals Tab ----------------------
with tabs[3]:
    st.header("📤 Referrals")
    with st.expander("🔍 Filter Referrals"):
        rparams = {
            "email_status": st.selectbox("Email Status", ["", "sent", "failed", "verified", "blocked"]),
            "response_status": st.selectbox("Response Status", ["", "waiting", "opened", "clicked", "replied", "ignored", "bounced"]),
            "critical": st.slider("Critical", 0, 5)
        }
        if st.button("Filter Referrals"):
            resp = requests.get(f"{BASE_URL}/referrals/", params=rparams)
            if resp.status_code == 200:
                referrals = resp.json()["results"]
                for r in referrals:
                    with st.expander(f"{r['candidate_name']} ({r['candidate_email']})"):
                        st.write(r)
                        with st.form(f"edit_ref_{r['id']}"):
                            updated = {
                                "email_status": st.selectbox("Email Status", ["sent", "failed", "verified", "blocked"], index=["sent", "failed", "verified", "blocked"].index(r["email_status"])),
                                "response_status": st.selectbox("Response", ["waiting", "opened", "clicked", "replied", "ignored", "bounced"], index=["waiting", "opened", "clicked", "replied", "ignored", "bounced"].index(r["response_status"])),
                                "critical": st.slider("Critical", 0, 5, r["critical"])
                            }
                            if st.form_submit_button("Update Referral"):
                                requests.put(f"{BASE_URL}/referrals/{r['id']}", json=updated)
                                st.success("Updated ✅")
                        if st.button(f"Delete Referral ID {r['id']}"):
                            requests.delete(f"{BASE_URL}/referrals/{r['id']}")
                            st.success("Deleted ✅")

# ---------------------- Users Tab ----------------------
with tabs[4]:
    st.header("👤 Users")
    with st.expander("🔍 Filter Users"):
        uparams = {
            "name": st.text_input("User Name Filter"),
            "email": st.text_input("User Email Filter")
        }
        if st.button("Filter Users"):
            resp = requests.get(f"{BASE_URL}/users/", params=uparams)
            if resp.status_code == 200:
                users = resp.json()["results"]
                for u in users:
                    with st.expander(f"{u['name']} ({u['email']})"):
                        st.write(u)
                        with st.form(f"edit_user_{u['id']}"):
                            updated = {
                                "name": st.text_input("Name", u["name"]),
                                "referral_credits": st.number_input("Referral Credits", value=u["referral_credits"], min_value=0)
                            }
                            if st.form_submit_button("Update User"):
                                requests.put(f"{BASE_URL}/users/{u['id']}", json=updated)
                                st.success("Updated ✅")
                        if st.button(f"Delete User ID {u['id']}"):
                            requests.delete(f"{BASE_URL}/users/{u['id']}")
                            st.success("Deleted ✅")
