console.log("Hello World");

$(document).ready(function(){
    // function to get the CSRF Token for all the patch request to be send later..
    function getCookie(name) {
        var cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            var cookies = document.cookie.split(';');
            for (var i = 0; i < cookies.length; i++) {
                var cookie = cookies[i].trim();
                // Does this cookie string begin with the name we want?
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }

    // Loading the Datatable..
    $('#example').DataTable({
        "order": [[0, "desc"]]
    });

    //View More Button Red On Click function..
    $(".lead-detail").click(function () {
        let leadid = this.id
        fetch(`/leads/${leadid}`)
            .then((response) => {
                return response.json();
            })
            .then((leadjson) => {
                let leadData = `<p>: <strong>${leadjson.first_name}</strong></p>
                <p>: <strong>${leadjson.last_name}</strong></p> <p> : <strong>${leadjson.type_of_enquiry}</strong></p><p> : <strong>${leadjson.company}</strong></p><p>: <strong>${leadjson.email}</strong></p><p> : <strong>${leadjson.phone}</strong></p><p>: <strong>${leadjson.positions_to_fill}</strong></p><p>: <strong>${leadjson.service_requirements}</strong></p><p>: <strong>${leadjson.loc_of_hire}</strong></p><p>: <strong>${leadjson.industry}</strong></p><p>: <strong>${leadjson.comp_emp_strength}</strong></p><p>: <strong>${leadjson.form_submission_time}</strong></p><p>: <strong>${leadjson.form_type }</strong></p>`
                $(".lead-data").html(leadData)
                let leadStatus = leadjson.status.name
                $('#leadStatus').text(leadStatus)
                $('#currentStatus').text(leadStatus)

                const csrftoken = getCookie('csrftoken');
                console.log(csrftoken)
                $("#submitStatus").click(function () {
                    console.log(`on click status value : ${$('#status').val()}`)
                    let newStatus = $('#status').val()
                    if (newStatus !== null) {
                        const data = { 
                            "status": newStatus
                        }
                        console.log(`to send a fetch PATCH with ${data.status}`)
                        fetch(`/leads/${leadid}/`, {
                            method: 'PATCH',
                            headers: {
                                'Content-Type': 'application/json',
                                'X-CSRFToken': csrftoken
                            },
                            body: JSON.stringify(data)
                        })
                        .then((response) => response.json())
                        .then((result) => {
                            console.log()
                            $('#leadStatus').text($("#status option:selected").html())
                            // $('#currentStatus').text(leadStatus)
                        })
                        .catch((error) => {
                            console.error('Error:', error);
                        });
                    }
                })
            })   
            .catch((error)=>{
                console.log(`Error : ${error} `)
            })    
        $("#myModal").modal();
    });

    //Reassign Button On Click Function
    $(".lead-reassign").click(function(){
        console.log(`reassign : ${this.id}`)
        let leadid = this.id
        const csrftoken = getCookie('csrftoken');
        //Fetching to whom the lead is currently assigned to..
        fetch(`/leads/${leadid}`)
            .then((response) => {
                return response.json();
            })
            .then((leadjson) => {         
                $('#leadSalesperson').text(leadjson.assigned_to[0].email)
            })
            .catch((error) => {
                console.log(`Error : ${error} `)
            })
            
        //Fetching the list of salesperson to whom we can reassign the lead..
        fetch(`/salespersons/`)
            .then((response) => {
                return response.json();
            })
            .then((salespersons) => {
                console.log(salespersons)
                const select = document.getElementById("salespersons"); 
                for (let i = 0; i < salespersons.length; i++) {
                    let opt = salespersons[i].email;
                    let el = document.createElement("option");
                    el.textContent = opt;
                    el.value = i+1;
                    select.appendChild(el);
                }                
            })
            .catch((error) => {
                console.log(`Error : ${error} `)
            })
        
        //Reassign Patch Request to ensure the lead is now reassigned to the new salesperson..
        $("#reassignSalesperson").click(function(){
            console.log(`on click selected salesperson : ${$('#salespersons').val()}`)
            let newSalesperson = $('#salespersons').val()
            if(newSalesperson !== null){
                const data = {
                    "assigned_to": [newSalesperson]
                }
                console.log(`to send a fetch PATCH with ${data.assigned_to}`)
                fetch(`/leads/${leadid}/`, {
                        method: 'PATCH',
                        headers: {
                            'Content-Type': 'application/json',
                            'X-CSRFToken': csrftoken
                        },
                        body: JSON.stringify(data)
                    })
                    .then((response) => response.json())
                    .then((result) => {
                        console.log(result)
                        $('#leadSalesperson').text($("#salespersons option:selected").html())
                    // $('#currentStatus').text(leadStatus)
                    })
                    .catch((error) => {
                        console.error('Error:', error);
                    });
            }
        })      
        $("#reassignModal").modal();
    })
});
