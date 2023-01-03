## Access Guide

To access the data gathered by this project you may use "db_connection_read.py" to access the MongoDB database.

#### Requirements
You will need pymongo, which can be installed with conda.

Tutorials on how to format queries can be found in the (documentation)[https://pymongo.readthedocs.io/en/stable/tutorial.html].

#### Instructions
With the file in your working directory, you can connect by adding the following lines to your script or jupyter notebook:
~~~
from db_connection import setup_client

client = setup_client()
db = client.cc_db
~~~
Now you are all set up to start querying the database. :)

#### Database Schema
There are 3 collections in the database:
- 'norms': This are the Norm Proposals with the extracted text from the PDF files.
Sample:
```
{'_id': '449-5',
 'commision': 'Comisión sobre Medio Ambiente',
 'name': 'Iniciativa Convencional Constituyente que incorpora el principio de planificación social prospectiva como elemento central de la planificación estatal económica, social y ambiental',
 'topic': 'Planificación social',
 'url': 'https://www.chileconvencion.cl/wp-content/uploads/2022/02/449-5-Iniciativa-Convencional-Constituyente-del-cc-Marcos-Barraza-sobre-Pp.-Planificacion-Social-1401-31-01.pdf',
 'signatures': 'Marcos Barraza Bessy Gallardo Prado Isabel Godoy Monardez más7',
 'signatures_id': [145, 148, 58, 114, 41, 88, 10, 17, 59, 112, 148, 94],
 'text': 'Here goes the text extracted from the PDF file'}
```

- 'members': Names of Assemblymembers. Note that in Chile people have their mother's maiden name as a 'fourth' name so that their full name is: given name ('Nombres'), middle name (not provided), paternal surname/family name ('ApellidoPaterno'), and maternal surname ('ApellidoPaterno'). 
Sample:
~~~
{'_id': ObjectId('623bdd8c25b9f275eab91986'),
 'ConvencionalId': '1',
 'ApellidoMaterno': 'González',
 'ApellidoPaterno': 'Abarca',
 'Nombres': 'Damaris'}
~~~
- 'voting_records': Details of all decisions put to a vote and their results, including the voting records of each individual member.
Sample:
```
{'_id': '6079',
 'NumeroSesion': '109',
 'Fecha': '2022-06-24T12:00:12'
 'Materia': 'Here goes the topic, a description of what is being voted on.'
 'Resultado': 'Here goes the result of the election, either "APROBADO" if it was approved, or "RECHAZADO" if it was rejected'
 'TotalAfirmativo: 'Here does the total number of votes for the motion'
 'TotalEnContra': 'Here does the total number of votes against the motion'
 'TotalAbastencion': 'Here does the total number of abstained/null votes',
 'TotalNoVota': 'Here does the total number missing votes due to nonappearance',
 'Votos': {
  {'Nombre': 'Abarca González, Damaris',
   'Votacion': 'Here goes whether the assemblymember voted for, against, null, or non-appearance'},
   ...
  {'Nombre': 'Abarca Riveros, Jorge',
   'Votacion': 'AFIRMATIVO'}
 }
}
```



Not all Norm Proposals in the 'norms' collection have assigned a list of the Assemblymembers that endorse it, so they will need to be detected in the extracted text (usually at the beginning or end of the text) if they are needed for your purposes.
Names within the text can be expressed in sometimes arbitrary formats. For example, if U.S. president were Chilean he would also have his mother's maiden name and his full name would be 'Joseph Robinette Biden Finnegan' and his name could also be expressed as:

- Joseph Biden  - (given name + paternal surname)
- Joseph Robinette Biden  - (given name + middle name + paternal surname)
- Joseph Biden Finnegan - (given name + paternal surname + maternal surname)
- Biden, Joseph - (paternal surname + ',' + given name)
- Biden, Joseph Robinette (paternal surname + ',' + given name + middle name)
- Biden Finnegan, Joseph - (paternal surname + maternal surname + ',' + given name)
- Biden Finnegan, Joseph Robinette - (paternal surname + maternal surname + ',' + given name + middle name)

Essentially:
- The given name and paternal surname are *always* present.
- The maternal surname is *usually* present and always follows the paternal given name. Colloquially it is skipped but usually present in legal settings, especially to differentiate between people who have the same paternal family name, same way the middle name initial is used in the U.S.
- The middle name is the more likely one to be missing, But if you're scanning the text in the Norm Proposals you will find most people use it when they sign their name, since it is part of their full legal name. This is usually the norm, but not all people, and not all the proposals follow this convention.


You must take this into consideration if you're looking to find the authors/endorsers of the Norm Proposals, probably tokenizing "quad-grams".
 


