This is a digital profile PDF generation application. Digital Profile is a comprehensive detailing of a municipality's demographics, infrastructure, and services. It is used to generate reports for various stakeholders including government officials, NGOs, and the public.

You will be implementing the following sections for the digital profile.

- Economic Section
The economic section has already the following contents:

1. major skills
2. municipalty wide foreign employment coutnries
3. remittance expenses
4. ward wise house base 
5. ward wise house outer wall 
6. ward wise house ownership

Each of these have their own individual files present as html.
these html are then combined at @economics_full_report.html which is then imported at the pdf_full_report.html.

So i need you to implement the following domains and such please.
The domains work in the following way:
- There is a management command that will put the following data.



४.५.४	सहकारी संस्थाहरूको विवरण

it has the following fields in the model:

- Cooperatives:
MunicipalityWideCooperatives with the following fields:
- name
- ward_number
- cooperative type

