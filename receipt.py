import streamlit as st
from fpdf import FPDF
from datetime import datetime

if "products" not in st.session_state:
    st.session_state.products = []

IMAGE_URL = "https://plus.unsplash.com/premium_vector-1761152893047-5a2de37258db?q=80&w=1153&auto=format&fit=crop&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D"
st.markdown("""
<style>

/* Aurora Background */
.stApp {
    background: linear-gradient(
135deg,
#4f46e5 0%,
#7c3aed 50%,
#ec4899 100%
);   
}
h1 {
    text-align: center;
    color: white !important;
    font-size: 4rem !important;
    font-weight: 800 !important;
    margin-bottom: 20px;
}

/* Subheaders */
h2, h3 {
    color: white !important;
}

/* Labels */
label {
    color: white !important;
    font-weight: 600;
}

/* Input fields */
.stTextInput input,
.stNumberInput input {
    border-radius: 12px;
    border: none;
    padding: 10px;
}

/* Buttons */
.stButton > button {
    width: 100%;
    border-radius: 12px;
    height: 50px;
    font-size: 18px;
    font-weight: bold;
    background: #ff6b6b;
    color: white;
    border: none;
}

/* Hover effect */
.stButton > button:hover {
    background: #ff5252;
}

/* Glass card */
.glass {
    background: rgba(255,255,255,0.15);
    backdrop-filter: blur(10px);
    padding: 20px;
    border-radius: 20px;
    border: 1px solid rgba(255,255,255,0.2);
}

</style>
""", unsafe_allow_html=True)

st.title("🧾 Receipt Generator")


# Input fields for receipt details
col1, col2 = st.columns(2)

with col1:
    customer_name = st.text_input("👤 Customer Name")

with col2:
    customer_phone = st.text_input("📞 Phone Number")
st.markdown("## 🛍️ Add Product")
payment_method = st.selectbox("💸Payment Method", ["Cash", "Card", "UPI"])

item_name = st.text_input("📦Item Name")
quantity = st.number_input("🛒Quantity", min_value=1, step=1)
price_per_item = st.number_input("Price per Item", min_value=0.0, step=0.01)

if st.button("Add Product➕"):
    if item_name.strip():
        st.session_state.products.append({
            "item": item_name,
            "qty": quantity,
            "price": price_per_item
        })



st.subheader("📋Products")

for product in st.session_state.products:
    amount = product["qty"] * product["price"]

    st.write(
        f"{product['item']} | "
        f"Qty: {product['qty']} | "
        f"Price: Rs.{product['price']:.2f} | "
        f"Amount: Rs.{amount:.2f}"
    )

if st.button("🗑️ Clear Products"):
    st.session_state.products = []
    st.rerun()

# Calculate total price
total_price = 0

for product in st.session_state.products:
    total_price += product["qty"] * product["price"]

gst_rate = 0.18
gst_amount = total_price * gst_rate


col1, col2, col3 = st.columns(3)

with col1:
    st.markdown(f"""
    <div class="metric-card">
        <h4>💰 Total</h4>
        <h2>Rs.{total_price:.2f}</h2>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown(f"""
    <div class="metric-card">
        <h4>📊 GST</h4>
        <h2>Rs.{gst_amount:.2f}</h2>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown(f"""
    <div class="metric-card">
        <h4>💵 Grand Total</h4>
        <h2>Rs.{total_price + gst_amount:.2f}</h2>
    </div>
    """, unsafe_allow_html=True)

# Generate receipt
if st.button("Generate Receipt 📄"):

    product_lines = ""

    for product in st.session_state.products:
        amount = product["qty"] * product["price"]

        product_lines += (
            f"{product['item']} | "
            f"{product['qty']} x "
            f"Rs.{product['price']:.2f} = "
            f"Rs.{amount:.2f}\n"
        )


product_lines = ""

for product in st.session_state["products"]:
    amount = product["qty"] * product["price"]

    product_lines += (
        f"Item: {product['item']}\n"
        f"Qty: {product['qty']}\n"
        f"Price: Rs.{product['price']:.2f}\n"
        f"Amount: Rs.{amount:.2f}\n"
        f"-------------------------\n"
    )

receipt = f"""
    Receipt
-----------------------------------
Customer Name: {customer_name}
Customer Phone: {customer_phone}
Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

Products:
{product_lines}

-----------------------------------
Total Price: Rs.{total_price:.2f}
GST Amount: Rs.{gst_amount:.2f}
Grand Total: Rs.{total_price + gst_amount:.2f}

Payment Method: {payment_method}

Thank you for your purchase!
VISIT AGAIN
"""

    

st.text(receipt)


    # PDF code goes here
#DOWNLOAD RECEIPT AS PDF
pdf = FPDF()
pdf.add_page()

# Draw receipt border
pdf.rect(35, 20, 140, 240)

# Move inside the box
pdf.set_xy(40, 25)

# Receipt title
pdf.set_font("Arial", "B", 18)
pdf.cell(130, 10, "RECEIPT(STORE NAME)", ln=True, align="C")

pdf.ln(5)

# Receipt content
pdf.set_font("Arial", "", 12)

for line in receipt.split("\n"):
    pdf.set_x(40)
    pdf.cell(130, 8, line, ln=True)
pdf_file_name = f"receipt.pdf"
pdf.output(pdf_file_name)
    
with open(pdf_file_name, "rb") as file:
        st.download_button(
            label="Download Receipt as PDF",
            data=file,
            file_name=pdf_file_name,
            mime="application/pdf"
        )


#    python -m streamlit run receipt.py