% rebase('base.tpl', title='CWD Email Edit/Add', refreshinterval=0, scripturl='')
<div class="container">
    <h5 class="center-align">Email Form</h5>
    <div class="row">
        <form class="col s12" method="post">
            <div class="row">
                <div class="input-field col s5">
                    <i class="material-icons prefix">person_pin</i>
                    <input placeholder="Your Name Here" id="name" name="name" type="text" class="validate"
                           value="{{ email.name if email else '' }}" required>
                    <label for="name">Name</label>
                </div>
                <div class="input-field col s5">
                    <input name="namematch" value="{{ email.namematch if email else '' }}" placeholder="%" id="matchregex" type="text"
                           class="validate" required>
                    <label for="matchregex">Jobname Match</label>
                </div>
                <div class="input-field col s2">
                    <p>
                        <input name="active" type="checkbox" id="active" checked/>
                        <label for="active">Active</label>
                    </p>
                </div>
            </div>
            <div class="row">
                <div class="input-field col s12">
                    <i class="material-icons prefix">email</i>
                    <input name="emailaddress" id="email" type="email" class="validate" value="{{ email.emailaddress if email else '' }}"
                           required>
                    <label for="email" data-error="Please Enter a valid email!">Email</label>
                </div>
            </div>
            <div class="row">
                <button class="btn waves-effect waves-light" type="submit">Submit
                    <i class="material-icons right">send</i>
                </button>
            </div>
        </form>
    </div>

</div>