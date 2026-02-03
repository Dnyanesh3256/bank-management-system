import streamlit as st
from bank import Bank

bank = Bank()

st.set_page_config(page_title="Bank Management System", layout="centered")
st.title("🏦 Bank Management System")

menu = st.sidebar.selectbox(
    "Select Action",
    [
        "Create Account",
        "Deposit Money",
        "Withdraw Money",
        "Show Details",  
        "Update Details",
        "Delete Account"
    ]
)


def auth_inputs():
    acc = st.text_input("Account Number")
    pin = st.text_input("PIN", type="password")
    return acc, pin

# ---------------- CREATE ACCOUNT ----------------
if menu == "Create Account":
    st.subheader("Create New Account")

    name = st.text_input("Name")
    age = st.number_input("Age", min_value=0)
    email = st.text_input("Email")
    pin = st.text_input("4-digit PIN", type="password")

    if st.button("Create Account"):
        success, res = bank.create_account(name, age, email, int(pin))
        if success:
            st.success("Account Created Successfully!")
            st.write("Account Number:", res["account_no"])
        else:
            st.error(res)

# ---------------- SHOW DETAILS ----------------
elif menu == "Show Details":
    st.subheader("Account Details")

    acc, pin = auth_inputs()

    if st.button("Show Details"):
        success, res = bank.show_details(acc, int(pin))
        if success:
            st.success("Account Found")
            for k, v in res.items():
                st.write(f"**{k}:** {v}")
        else:
            st.error(res)

# ---------------- DEPOSIT ----------------
elif menu == "Deposit Money":
    st.subheader("Deposit Money")
    acc, pin = auth_inputs()
    amount = st.number_input("Amount", min_value=0)

    if st.button("Deposit"):
        success, res = bank.deposit(acc, int(pin), amount)
        st.success(f"New Balance: ₹{res}") if success else st.error(res)

# ---------------- WITHDRAW ----------------
elif menu == "Withdraw Money":
    st.subheader("Withdraw Money")
    acc, pin = auth_inputs()
    amount = st.number_input("Amount", min_value=0)

    if st.button("Withdraw"):
        success, res = bank.withdraw(acc, int(pin), amount)
        st.success(f"Remaining Balance: ₹{res}") if success else st.error(res)

# ---------------- UPDATE ----------------
elif menu == "Update Details":
    st.subheader("Update Account Details")
    acc, pin = auth_inputs()

    new_name = st.text_input("New Name (optional)")
    new_email = st.text_input("New Email (optional)")
    new_pin = st.text_input("New PIN (optional)", type="password")

    if st.button("Update"):
        success, res = bank.update_details(
            acc,
            int(pin),
            name=new_name or None,
            email=new_email or None,
            new_pin=int(new_pin) if new_pin else None
        )
        st.success(res) if success else st.error(res)

# ---------------- DELETE ----------------
elif menu == "Delete Account":
    st.subheader("Delete Account")
    acc, pin = auth_inputs()

    if st.button("Delete"):
        success, res = bank.delete_account(acc, int(pin))
        st.success(res) if success else st.error(res)
