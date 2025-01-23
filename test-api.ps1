
$port = 5003

Invoke-RestMethod http://localhost:5002/api/v1/contacts -Method Get


Invoke-RestMethod -Uri http://localhost:5002/api/v1/contacts -Method Post `
    -Body @{ 
        first_name = 'Alan'
        last_name = 'Kay'
        phone = '123-456-7890'
        email = 'alan1@smalltalk.org' 
    }

Invoke-RestMethod "http://localhost:$port/api/v1/contacts/5" -Method Get


Invoke-RestMethod -Uri "http://localhost:$port/api/v1/contacts/9" -Method put `
    -Body @{ 
        first_name = 'Bill'
        last_name = 'Joy'
        phone = '123-456-7890'
        email = 'bill@bsd.org' 
    }




Invoke-RestMethod -Uri "http://localhost:$port/api/v1/contacts/9" -Method post `
    -Body @{ 
        first_name = 'Bill'
        last_name = 'Joy'
        phone = '123-456-7890'
        email = 'bill@bsd.org' 
    }


# Invoke-RestMethod -Uri "http://localhost:5020/api/v1/contacts/15" -Method put `
#     -Body @{ 
#         first_name = 'Bill'
#         last_name = 'Joy'
#         phone = '123-456-7890'
#         email = 'bill@bsd.org' 
#     }


Invoke-RestMethod -Uri "http://localhost:$port/api/v1/contacts/6" -Method Delete
