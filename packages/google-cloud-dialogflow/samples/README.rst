Dialogflow: Python Samples
=============================

Dialogflow samples using python client.

Table of Contents
-----------------

-  `Before you begin <#before-you-begin>`__
-  `Samples <#samples>`__

   -  `Detect intent (texts) <#detect-intent-texts>`__
   -  `Detect intent (audio) <#detect-intent-audio>`__
   -  `Detect intent (streaming) <#detect-intent-streaming>`__
   -  `Intent management <#intent-management>`__
   -  `Entity type management <#entity-type-management>`__
   -  `Entity management <#entity-management>`__
   -  `Session entity type management <#session-entity-type-management>`__

Before you begin
----------------

#. Before running the samples, make sure you’ve followed the steps in
   the `Before you begin section <../README.rst#before-you-begin>`__ of
   the client library’s README.

#. If your project does not already have an agent, create one following
   the `instructions <https://dialogflow.com/docs/getting-started/building-your-first-agent#create_an_agent>`__.

   (If you want to create an enterprise agent, follow `these instructions <https://cloud.google.com/dialogflow-enterprise/docs/quickstart>`__.)

#. This sample comes with a `sample agent <./resources/RoomReservation.zip>`__
   which you can use to try the samples with.  Following the instructions on `this page <https://dialogflow.com/docs/best-practices/import-export-for-versions>`__
   to import the agent from the `console <https://console.dialogflow.com>`__.

	**WARNING: Importing the sample agent will add intents and entities to your Dialogflow agent. You might want to use a different Google Cloud Platform Project, or export your Dialogflow agent before importing the sample agent to save a version of your agent before the sample agent was imported.**

Samples
-------

Detect intent (texts)
~~~~~~~~~~~~~~~~~~~~~

View the `source code <detect_intent_texts.py>`__.

**Usage:** ``python detect_intent_texts.py --help``

.. code-block::

	usage: detect_intent_texts.py [-h] --project-id PROJECT_ID
	                              [--session-id SESSION_ID]
	                              [--language-code LANGUAGE_CODE]
	                              texts [texts ...]

	DialogFlow API Detect Intent Python sample with text inputs.

	Examples:
	  python detect_intent_texts.py -h
	  python detect_intent_texts.py --project-id PROJECT_ID   --session-id SESSION_ID   "hello" "book a meeting room" "Mountain View"
	  python detect_intent_texts.py --project-id PROJECT_ID   --session-id SESSION_ID   "tomorrow" "10 AM" "2 hours" "10 people" "A" "yes"

	positional arguments:
	  texts                 Text inputs.

	optional arguments:
	  -h, --help            show this help message and exit
	  --project-id PROJECT_ID
	                        Project/agent id. Required.
	  --session-id SESSION_ID
	                        Identifier of the DetectIntent session. Defaults to a
	                        random UUID.
	  --language-code LANGUAGE_CODE
	                        Language code of the query. Defaults to "en-US".
	
Detect intent (audio)
~~~~~~~~~~~~~~~~~~~~~

View the `source code <detect_intent_audio.py>`__.

**Usage:** ``python detect_intent_audio.py --help``

.. code-block::

	usage: detect_intent_audio.py [-h] --project-id PROJECT_ID
	                              [--session-id SESSION_ID]
	                              [--language-code LANGUAGE_CODE]
	                              --audio-file-path AUDIO_FILE_PATH

	DialogFlow API Detect Intent Python sample with audio file.

	Examples:
	  python detect_intent_audio.py -h
	  python detect_intent_audio.py --project-id PROJECT_ID   --session-id SESSION_ID --audio-file-path resources/book_a_room.wav
	  python detect_intent_audio.py --project-id PROJECT_ID   --session-id SESSION_ID --audio-file-path resources/mountain_view.wav
	  python detect_intent_audio.py --project-id PROJECT_ID   --session-id SESSION_ID --audio-file-path resources/today.wav

	optional arguments:
	  -h, --help            show this help message and exit
	  --project-id PROJECT_ID
	                        Project/agent id. Required.
	  --session-id SESSION_ID
	                        Identifier of the DetectIntent session. Defaults to a
	                        random UUID.
	  --language-code LANGUAGE_CODE
	                        Language code of the query. Defaults to "en-US".
	  --audio-file-path AUDIO_FILE_PATH
	                        Path to the audio file.

Detect intent (streaming)
~~~~~~~~~~~~~~~~~~~~~~~~~

View the `source code <detect_intent_stream.py>`__.

**Usage:** ``python detect_intent_stream.py --help``

.. code-block::

	usage: detect_intent_stream.py [-h] --project-id PROJECT_ID
	                               [--session-id SESSION_ID]
	                               [--language-code LANGUAGE_CODE]
	                               --audio-file-path AUDIO_FILE_PATH

	DialogFlow API Detect Intent Python sample with audio files processed
	as an audio stream.

	Examples:
	  python detect_intent_stream.py -h
	  python detect_intent_stream.py --project-id PROJECT_ID   --session-id SESSION_ID --audio-file-path resources/book_a_room.wav
	  python detect_intent_stream.py --project-id PROJECT_ID   --session-id SESSION_ID --audio-file-path resources/mountain_view.wav

	optional arguments:
	  -h, --help            show this help message and exit
	  --project-id PROJECT_ID
	                        Project/agent id. Required.
	  --session-id SESSION_ID
	                        Identifier of the DetectIntent session. Defaults to a
	                        random UUID.
	  --language-code LANGUAGE_CODE
	                        Language code of the query. Defaults to "en-US".
	  --audio-file-path AUDIO_FILE_PATH
	                        Path to the audio file.

Intent management
~~~~~~~~~~~~~~~~~

View the `source code <intent_management.py>`__.

**Usage:** ``python intent_management.py --help``

.. code-block::

	usage: intent_management.py [-h] --project-id PROJECT_ID
	                            {list,create,delete} ...

	DialogFlow API Intent Python sample showing how to manage intents.

	Examples:
	  python intent_management.py -h
	  python intent_management.py --project-id PROJECT_ID list
	  python intent_management.py --project-id PROJECT_ID create   "room.cancellation - yes"   --training-phrases-parts "cancel" "cancellation"   --message-texts "Are you sure you want to cancel?" "Cancelled."
	  python intent_management.py --project-id PROJECT_ID delete   74892d81-7901-496a-bb0a-c769eda5180e

	positional arguments:
	  {list,create,delete}
	    list
	    create              Create an intent of the given intent type.
	    delete              Delete intent with the given intent type and intent
	                        value.

	optional arguments:
	  -h, --help            show this help message and exit
	  --project-id PROJECT_ID
	                        Project/agent id. Required.

Entity type management
~~~~~~~~~~~~~~~~~~~~~~

View the `source code <entity_type_management.py>`__.

**Usage:** ``python entity_type_management.py --help``

.. code-block::

	usage: entity_type_management.py [-h] --project-id PROJECT_ID
	                                 {list,create,delete} ...

	DialogFlow API EntityType Python sample showing how to manage entity types.

	Examples:
	  python entity_type_management.py -h
	  python entity_type_management.py --project-id PROJECT_ID list
	  python entity_type_management.py --project-id PROJECT_ID create employee
	  python entity_type_management.py --project-id PROJECT_ID delete   e57238e2-e692-44ea-9216-6be1b2332e2a

	positional arguments:
	  {list,create,delete}
	    list
	    create              Create an entity type with the given display name.
	    delete              Delete entity type with the given entity type name.

	optional arguments:
	  -h, --help            show this help message and exit
	  --project-id PROJECT_ID
	                        Project/agent id. Required.

Entity management
~~~~~~~~~~~~~~~~~

View the `source code <entity_management.py>`__.

**Usage:** ``python entity_management.py --help``

.. code-block::

	usage: entity_management.py [-h] --project-id PROJECT_ID
	                            {list,create,delete} ...

	DialogFlow API Entity Python sample showing how to manage entities.

	Examples:
	  python entity_management.py -h
	  python entity_management.py --project-id PROJECT_ID   list --entity-type-id e57238e2-e692-44ea-9216-6be1b2332e2a
	  python entity_management.py --project-id PROJECT_ID   create new_room --synonyms basement cellar   --entity-type-id e57238e2-e692-44ea-9216-6be1b2332e2a
	  python entity_management.py --project-id PROJECT_ID   delete new_room   --entity-type-id e57238e2-e692-44ea-9216-6be1b2332e2a

	positional arguments:
	  {list,create,delete}
	    list
	    create              Create an entity of the given entity type.
	    delete              Delete entity with the given entity type and entity
	                        value.

	optional arguments:
	  -h, --help            show this help message and exit
	  --project-id PROJECT_ID
	                        Project/agent id. Required.

Session entity type management
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

View the `source code <session_entity_type_management.py>`__.

**Usage:** ``python session_entity_type_management.py --help``

.. code-block::

	usage: session_entity_type_management.py [-h] --project-id PROJECT_ID
	                                         {list,create,delete} ...

	DialogFlow API SessionEntityType Python sample showing how to manage
	session entity types.

	Examples:
	  python session_entity_type_management.py -h
	  python session_entity_type_management.py --project-id PROJECT_ID list   --session-id SESSION_ID
	  python session_entity_type_management.py --project-id PROJECT_ID create   --session-id SESSION_ID   --entity-type-display-name room --entity-values C D E F
	  python session_entity_type_management.py --project-id PROJECT_ID delete   --session-id SESSION_ID   --entity-type-display-name room

	positional arguments:
	  {list,create,delete}
	    list
	    create              Create a session entity type with the given display
	                        name.
	    delete              Delete session entity type with the given entity type
	                        display name.

	optional arguments:
	  -h, --help            show this help message and exit
	  --project-id PROJECT_ID
	                        Project/agent id. Required.

