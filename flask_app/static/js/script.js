var regForm = document.getElementById('regForm')
regForm.onsubmit = function(e) {
    e.preventDefault() // keep form from submitting and reseting page
    var form = new FormData(regForm) // creates formdata object to send through fetch
    fetch('http://127.0.0.1:5001/register', {method : 'POST', body : form})
        .then(response => {
            if(response.redirected) {
                window.location = response.url
            } 
            return response.json()
        } )
        .then(data => {
            let parent = document.getElementById('reg_errors') // get the div where error messages are displayed
            while (parent.firstChild) { // removes firstChild until there are no more children
                parent.removeChild(parent.firstChild);
            }
            data.messages.forEach(element => { // create a p tag for each error message
                console.log(element)
                let this_p = document.createElement('p')
                this_p.innerHTML = element
                parent.appendChild(this_p) // add p tag to parent div
            })
            
        })

}

var logForm = document.getElementById('logForm')
logForm.addEventListener('submit', (e) => {
    e.preventDefault() // keep from from default behavior
    var form = new FormData(logForm) // creates fromdata obect to send throug fetch
    fetch('http://127.0.0.1:5001/login', {method: 'POST', body : form})
        .then(response => {
            if(response.redirected) {
                window.location = response.url
            } 
            return response.json()} )
        .then(data => {
            
            console.log(data)
            let parent = document.getElementById('login_errors')
            while (parent.firstChild) {
                parent.removeChild(parent.firstChild) //remove each child node to clear error messages
            }
            let error = document.createElement('p')
            error.innerHTML = data.message
            parent.appendChild(error)
        })
})