

function addPerson(n) {
    // get the button that got clicked
    const div_to_change = document.getElementById(`addPerson${n}`);

    // turn the button into a new person field
    new_output = `
        <div class='form-group py-3 pl-3'>
            <h3>Person ${n}</h3>

            <div class='form-group'>
                <label for='street${n}'>Street Address</label>
                <input id='street${n}' type="text" class="form-control" name="street${n}"/>
            </div>

            <div class='form-group'>
                <label for='city${n}'>City</label>
                <input id='city${n}' type="text" class="form-control" name="city${n}" required/>
            </div>

            <div class='form-group'>
                <label for='state${n}'>State</label>
                <input id='state${n}' type="text" class="form-control" name="state${n}" required/>
            </div>

            <div class='form-group'>
                <label for='zip${n}'>Zip Code</label>
                <input id='zip${n}' type="text" class="form-control" name="zip${n}" />
            </div>
            
            <div class='pt-3'>
                <button class='btn btn-danger' type='button' onclick="removePerson(${n})">Remove Person</button>
            </div>
        </div>
    `
    if (n < 5) {
        new_output += `
            <div id='addPerson${n+1}'>
                <button class='btn btn-secondary' type='button' id='addPerson${n+1}' onclick="addPerson(${n+1})">Add person</button>
            </div>
        `
    }

    div_to_change.innerHTML = new_output
}


function removePerson(n) {
    const div_to_change = document.getElementById(`addPerson${n}`);

    div_to_change.innerHTML = `<button class='btn btn-secondary' type='button' onclick="addPerson(${n})">Add person</button>`
}

function showInfo(div_id) {
    const div_to_change = document.getElementById(div_id);
    if (div_to_change.style.visibility == "hidden") {
        div_to_change.style.visibility = "visible"
    }
    else {
        div_to_change.style.visibility = "hidden"
    }
}