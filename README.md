# check_python_kivy_app
application with python kivy for mobile checking moving parts and details 
plan to change table structure of application. Now we has two tables named "sent" for parts which goes from department 1 to deps 211, 210... and "details" for parts which arrives from deps 210, 211 to 1
and i want to add one table named "unit" which consist of two columns named "id" consist of autoincrement ids, and "number_name" consist of number detail and name each detail. This table we need for memory saving, dont save in table send or details number detail and name detail, but using for this only id.
and need to add table named "inclusion" which consist of four columns: "id", "parent_id" consist of number id from table unit, "child_id" consist of number id from table unit, "quantity" column consist of digit, this page say us how many child-parts need for making 1 parent-part 
