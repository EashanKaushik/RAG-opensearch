var apigClient = apigClientFactory.newClient();

function runQuery(){

    var inputValue = document.getElementById('queryInput').value;
    
    var ulElement = document.getElementById('elementList');
    ulElement.innerHTML = '';


    if (inputValue.trim() === "") {
        // Display an alert if the value is empty
        alert('Please enter query before submitting.');
    } else {
        // Display the value in the console (you can use it as needed)
        console.log('Text Value:', inputValue);

        // You can also use the value in other ways, for example, update the DOM
        // document.getElementById('output').innerText = inputValue;
    var params = {
            //This is where any header, path, or querystring request params go. The key is the parameter named as defined in the API
            text: inputValue
        };
        var body = {
            //This is where you define the body of the request
        };
        var additionalParams = {
            //If there are any unmodeled query parameters or headers that need to be sent with the request you can add them here
            headers: {
        
            },
            queryParams: {
        
            }
        };
        
        apigClient.queryGet(params, body, additionalParams)
            .then(function(result){
                console.log(result['data']);

                for(let i = 0; i < result['data'].length; i++){
                    getDocumentText(result['data'][i]['document_id']);
                }

            }).catch( function(result){
                //This is where you would put an error callback
                alert(result);
            });
        };
}

function getDocumentText(document_id){
    var params = {
        //This is where any header, path, or querystring request params go. The key is the parameter named as defined in the API
        document_id: document_id
    };
    var body = {
        //This is where you define the body of the request
    };
    var additionalParams = {
        //If there are any unmodeled query parameters or headers that need to be sent with the request you can add them here
        headers: {
    
        },
        queryParams: {
    
        }
    };
    var listItem = document.createElement('li');
    

    // Add the new list item to the existing list
    apigClient.documentGet(params, body, additionalParams)
        .then(function(result){
            listItem.className = 'list-group-item';
            console.log(result['data']['text']);
            listItem.textContent = result['data']['text']; 
            document.getElementById('elementList').appendChild(listItem);
           
        }).catch( function(result){
            //This is where you would put an error callback
            alert(result);
        });
}



function uploadDocument(){
    var inputValue = document.getElementById('documentTextarea').value;
    
    if (inputValue.trim() === "") {
        // Display an alert if the value is empty
        alert('Please enter document before submitting.');
    } else {
        var params = {
            //This is where any header, path, or querystring request params go. The key is the parameter named as defined in the API
            document: inputValue
        };
        var body = {
            //This is where you define the body of the request
        };
        var additionalParams = {
            //If there are any unmodeled query parameters or headers that need to be sent with the request you can add them here
            headers: {
        
            },
            queryParams: {
        
            }
        };
        
        apigClient.uploadGet(params, body, additionalParams)
            .then(function(result){
                console.log(result);
                alert(result['data']);
            }).catch( function(result){
                //This is where you would put an error callback
                alert(result);
            });
    };
}