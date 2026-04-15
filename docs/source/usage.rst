Installation
=====

.. _installation:

Lien Github
------------

Pour commencer rendez vous sur ce lien github : https://github.com/Raythe7/FabLab/

Installation du fichier de l'extention
----------------
Une fois sur la page github appuier sur le bouton vert "code"

Et puis sur Télécharger le dossier zip 

Une fois ce dossier installer faire le raccourcis Windows + R

Une fenêtres à l'intérieur et rentrer " %appdata% "

cele vous ouvre l'explorateur de fichier 

To retrieve a list of random ingredients,
you can use the ``lumache.get_random_ingredients()`` function:

.. autofunction:: lumache.get_random_ingredientsS

The ``kind`` parameter should be either ``"meat"``, ``"fish"``,
or ``"veggies"``. Otherwise, :py:func:`lumache.get_random_ingredients`
will raise an exception.

.. autoexception:: lumache.InvalidKindError

For example:

>>> import lumache
>>> lumache.get_random_ingredients()
['shells', 'gorgonzola', 'parsley']

