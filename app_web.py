from sqlalchemy.engine import result
import database
import streamlit as st
import analytics

database.init_db()
database.init_users_table()

if "user_id" not in st.session_state:
    st.title("💸 Personal Finance Dashboard")
    tab1,tab2 = st.tabs(["🔑 Login","📝 Register"])
    with tab1:
        st.subheader("Welcome Back!")
        login_email = st.text_input("Email",key = "login_email")
        login_password = st.text_input("Password",type='password',key="login_pass")
        if st.button("Login"):
            if login_email and login_password:
                result = database.login_user(login_email,login_password)
                if result :
                    st.session_state["user_id"] = result[0]
                    st.session_state["user_name"]=result[1]
                    st.rerun()
                else:
                    st.error("❌ Incorrect email or password.")
            else:
                st.error("Please fill in all feilds.")
    with tab2:
        st.subheader("Create New Account")
        reg_name = st.text_input("Your Name",key="reg_name")
        reg_email = st.text_input("Email",key="reg_email")
        reg_password = st.text_input("Password",type='password',key='reg_pass1')
        reg_password2 = st.text_input("Conform Password",type='password',key='reg_pass2')
        if st.button("Register"):
            if reg_name and reg_email and reg_password:
                if reg_password !=reg_password2:
                    st.error("❌ Passwords don't match!")
                else:
                    user_id = database.register_user(reg_name,reg_email,reg_password)
                    if user_id:
                        st.session_state['user_id'] = user_id
                        st.session_state['user_name'] = reg_name
                        st.rerun()
                    else:
                        st.error("❌ An account with this email already exists. Please login instead.")
            else:
                st.error("Please fill all feilds.")
    st.stop()
user_id = st.session_state["user_id"]
user_name = st.session_state["user_name"]

st.sidebar.write(f"Logged in as: **{user_name}")
if st.sidebar.button("Logout"):
    del st.session_state["user_id"]
    del st.session_state["user_name"]
    st.rerun()

st.title("💸 Personal Finance Dashboard")
st.header("Add a new Expense")
col1 , col2, col3=st.columns(3)
with col1:
    amount = st.number_input("Amount",min_value=0.0,format="%.2f")
with col2:
    category = st.text_input("Category (e.g.,Food,Rent )")
with col3:
    date = st.date_input("Date")
if st.button("Add Expenses"):
    if category:
        database.save_to_db(amount,category,str(date),user_id)
        st.success(f"Successfully added ${amount} for {category}!")
    else:
        st.error("Please enter a category.")

st.header("Expenses History")

df = database.load_from_db(user_id)
if not df.empty:
    df = df.reset_index()
    df.index = df.index + 1
    df.index.name = "No."
st.sidebar.header("🔍 Filter Expenses")
if not df.empty:
    category=['All'] + df['category'].unique().tolist()
    selected_category = st.sidebar.selectbox("Filter by category",category)
    if selected_category != "All":
        df = df[df['category'] == selected_category]
st.sidebar.header("🎯 Set Monthly Budget")
with st.sidebar.form("budget_form"):
    budget_cat = st.text_input("Category (e.g., Food)")
    budget_limit= st.number_input("Limit",min_value=0.0,format="%.2f")
    if st.form_submit_button("Save Budget"):
        if budget_cat:
            database.set_budget(budget_cat,budget_limit,user_id)
            st.sidebar.success(f"Budget for {budget_cat} set to ${budget_limit}")
        else:
            st.sidebar.error("Please enter a category")
if not df.empty:
    st.dataframe(df.drop(columns=['id']) , width="stretch")
else:
    st.info("No expenses found yet. Add one above ")
st.header("🎯 Budget Progress")
budgets = database.get_budgets(user_id)
if budgets:
    for cat ,limit in budgets.items():
        spent = df[df["category"] == cat ]['amount'].sum() if not df.empty else 0
        st.write(f"**{cat} : **${spent:.2f}/${limit:.2f}")
        progress_percentage = min(spent/limit,1.0) if limit > 0 else 0
        st.progress(progress_percentage)
else:
    st.info("NO budget set yet. Use the sidebar to set one! ")



st.header("✏️ Edit or Delete an Expense")
if not df.empty:
    row_no = st.number_input("Enter Expenses No. to Edit",min_value=1,max_value=len(df),step=1)
    edit_col1,edit_col2,edit_col3 = st.columns(3)
    with edit_col1:
        new_amount = st.number_input("New Amount",min_value=0.0,format="%.2f",key="edit_amount")
    with edit_col2:
        new_category = st.text_input("New Category",key="edit_category")
    with edit_col3:
        new_date = st.date_input("New Date",key="edit_date")
    btn_col1 , btn_col2 = st.columns(2)
    with btn_col1:

        if st.button("Update Expenses"):
            if new_category:
                real_db_id = df.loc[row_no,"id"]
                database.update_expenses(real_db_id,new_amount,new_category,str(new_date),user_id)
                st.success(f"Expense #{int(row_no)} updated successfully!")
                st.rerun()
            else:
                st.error("Plese enter a category.")
    with btn_col2:
        if st.button("🗑️ Delete Expense"):
            real_db_id = df.loc[row_no,'id'] 
            database.delete_expenses(real_db_id,user_id)
            st.success(f"Expense #{int(row_no)} deleted successfully!")
            st.rerun()     
else:
    st.info("No expenses to edit yet.")

st.header("📊 Analytics")
if not df.empty:
    chart_col1 ,chart_col2 = st.columns(2)
    with chart_col1:
        st.subheader("Spending by category")
        category_totals = df.groupby("category")['amount'].sum()
        st.bar_chart(category_totals)
    with chart_col2:
        st.subheader("Daily Spending")
        daily_totals = df.groupby("date")['amount'].sum()
        st.line_chart(daily_totals)