import streamlit as st
from hello import BankDB

BankDB.load()

st.sidebar.title("🏦 Simple Bank")
action = st.sidebar.selectbox("What do you want to do?", [
    "Create Account", "Deposit", "Withdraw", "Show Details"
])

if action == "Create Account":
    st.header("Create a new account")
    name = st.text_input("Name")
    age = st.number_input("Age", min_value=0, step=1)
    email = st.text_input("Email")
    pin = st.text_input("4‑digit PIN", type="password")

    if st.button("Create"):
        try:
            account = BankDB.create_account(name, age, email, int(pin))
            st.success(f"Account created! 🎉 Your account number is {account['accountNo']}")
        except Exception as e:
            st.error(str(e))

else:
    st.header(action)
    acct_no = st.text_input("Account number")
    pin = st.text_input("PIN", type="password")

    if st.button("Submit"):
        user = BankDB.find_user(acct_no, int(pin) if pin.isdigit() else -1)
        if not user:
            st.error("Wrong account or PIN")
        else:
            if action == "Deposit":
                amt = st.number_input("Deposit amount", value=0, min_value=0, step=1)
                if st.button("Deposit Now"):
                    try:
                        BankDB.deposit(user, amt)
                        st.success(f"Deposited ₹{amt}. New balance: ₹{user['balance']}")
                    except Exception as e:
                        st.error(str(e))

            elif action == "Withdraw":
                amt = st.number_input("Withdraw amount", value=0, min_value=0, step=1)
                if st.button("Withdraw Now"):
                    try:
                        BankDB.withdraw(user, amt)
                        st.success(f"Withdrew ₹{amt}. New balance: ₹{user['balance']}")
                    except Exception as e:
                        st.error(str(e))

            elif action == "Show Details":
                st.write(user)
