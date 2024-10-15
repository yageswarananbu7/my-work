import qrcode
import cv2
from pyzbar.pyzbar import decode

# Create a QR code with your email
email = "578@gmail.com"
qr = qrcode.QRCode(version=1, box_size=10, border=5)
qr.add_data(email)
qr.make(fit=True)

# Save the QR code as an image
img = qr.make_image(fill='black', back_color='white')
img_path = "email_qr.png"  # Save as a local file
img.save(img_path)
print("QR code generated and saved as email_qr.png")

# Load the image of the QR code
img_cv = cv2.imread(img_path)

# Decode the QR code
decoded_objects = decode(img_cv)

# Loop over all decoded objects and print data (email)
for obj in decoded_objects:
    print(f"QR Code data: {obj.data.decode('utf-8')}")

# Display the QR code image
cv2.imshow("QR Code", img_cv)
cv2.waitKey(0)
cv2.destroyAllWindows()


