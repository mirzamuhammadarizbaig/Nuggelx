# Generates a SAMPLE menu PDF. Replace data/nugglex_menu.pdf with your real one.
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
lines = """NUGGLEX RESTAURANT - MENU & INFO

About: NUGGLEX is a fast-food restaurant famous for crispy chicken nuggets. Located in Karachi, Pakistan.
Timings: Open daily 12:00 PM to 1:00 AM. Open all week including Fridays.
Delivery: Free delivery within 5 km on orders above Rs. 1000. Delivery takes 30-45 minutes.
Payment: Cash on delivery, JazzCash, Easypaisa and cards accepted.

NUGGETS
Classic Nuggets (6 pcs) - Rs. 450
Classic Nuggets (12 pcs) - Rs. 850
Spicy Nuggets (6 pcs) - Rs. 500
Cheese Stuffed Nuggets (6 pcs) - Rs. 650

BURGERS
Nuggle Burger - Rs. 600
Zinger Burger - Rs. 550
Double Crunch Burger - Rs. 800

SIDES AND DRINKS
Fries (regular) - Rs. 200
Fries (large) - Rs. 300
Coleslaw - Rs. 150
Soft drink (345 ml) - Rs. 120
Mint Margarita - Rs. 250

DEALS
Nugget Buddy Deal: 12 nuggets, 2 fries, 2 drinks - Rs. 1500
Student Deal: Nuggle Burger, fries and drink - Rs. 850 (show student card)
Family Feast: 24 nuggets, 4 fries, 1 liter drink - Rs. 2800

ALLERGY INFO
Nuggets contain gluten and egg. Cheese Stuffed Nuggets contain milk. All food is halal.
""".split("\n")
c = canvas.Canvas("data/nugglex_menu.pdf", pagesize=A4)
y = 800
for l in lines:
    if y < 50: c.showPage(); y = 800
    c.setFont("Helvetica-Bold" if l.isupper() else "Helvetica", 11)
    c.drawString(40, y, l); y -= 18
c.save()
