import Image
reminder_img = "remind1.gif"
out_image = "final.gif"
blank_image = Image.open("blank.gif")
blank_image.paste(reminder_img,(0,0))
blank_image.paste(reminder_img,(400,0))
blank_image.paste(reminder_img,(0,400))
blank_image.paste(reminder_img,(400,400))
blank_image.save(out_image)

