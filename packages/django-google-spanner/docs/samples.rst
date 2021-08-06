Sample Code
####################################

Create and register your first model
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
To define your database layout create a models file in your app folder and add the relevant 
classes to it. Spanner works exactly like any other database you may have used with Django. 
Here is a simple example you can run with Spanner. In our poll application below we create 
the following two models:

.. code:: python

    from django.db import models
    
    class Question(models.Model):
        question_text = models.CharField(max_length=200)
        pub_date = models.DateTimeField('date published')
        def __str__(self):
            return str(self.rating)
    
    class Choice(models.Model):
        question = models.ForeignKey(Question, on_delete=models.CASCADE)
        choice_text = models.CharField(max_length=200)
        votes = models.IntegerField(default=0)
