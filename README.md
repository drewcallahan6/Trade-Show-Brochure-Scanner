# Trade-Show-Brochure-Scanner

Overview: 

The Trade-Show-Brochure-Scanner is a python application which utilizes the PyQt4 GUI and pytesseract Optical Character Recognition (OCR) to aid in the automation of a time-consuming scanning and documenting process for the Engineering Department of Griffith Foods Inc.

Problem:

When engineers in the Griffith Foods Engineering Department visit trade shows, they naturally return with an abundance of brochures detailing various machinery, systems, and vendors.  With the recent advent of an internal, cloud-based database, the Engineering Department was seeking the documentation of these brochures on that database.  A ubiquitous format was established to make user interface more easily accessible.  The format is exampled below.

TITLE:

Known Locations Used:

Purpose:

Key Selection Criteria:
	-Point 1
	-Point 2

Vendor:

However, there is still the arduous task of documenting these brochures into this unique format. 

Solution:

The Trade-Show-Brochure-Scanner solves this problem by creating a user-friendly, Windows application that when run asks the user to upload a .jpg or .png scan of the brochure.  Once completed, the application automatically runs and picks out all the relevant information to piece into the format above.  The application returns all this information, in the correct format, to an editable text window that can then be uploaded to the cloud-based database. 

How to Use and How it Works:

The Trade-Show-Brochure-Scanner is available as an .exe file that when run first displays a home window.  This home window has a detailed description outlining the general process that one must follow.  Ultimately, this process involves initially scanning the brochures as .jpg or .png files and uploading them to the application.  Once the scan is uploaded, the program automatically runs using OCR to create a .txt file.  This file can then be used to look for the relevant information to fill out the established format.
As most brochures do not exhibit the same style or information divisions, it is integral that one looks for very general stylistic elements that reveal the locations of the title, purpose, vendor, etc.  And once all the information is extracted, the editor is opened and the result is displayed.  As previously mentioned, this text and can then be edited and copied to the database. 

