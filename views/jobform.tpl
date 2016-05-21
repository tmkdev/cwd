% rebase('base.tpl', title='CWD Job Edit', refreshinterval=0, scripturl='')
<div class="container">
    <h4 class="center-align">Job Form</h4>
    <h5 class="center-align">{{ jobname }}</h5>
    <div class="row">
        <form class="col s12" action="{{ get_url('/jobedit') }}" method="post">
            <div class="row">
                <div class="input-field col s5">
                    <i class="material-icons prefix">person_pin</i>
                    <input placeholder="Job Period in Minutes" id="period" name="period" type="number" class="validate"
                           value="{{ job.period if job else '' }}" required>
                    <label for="period">Job Period</label>
                </div>
                <div class="input-field col s5">
                    <input name="sla" value="{{ job.sla if job else '' }}" placeholder="SLA Max Runtime in Minutes" id="sla" type="number"
                           class="validate" required>
                    <label for="sla">Job SLA period</label>
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
                    <input name="description" id="description" type="text" class="validate" value="{{ job.description if job else '' }}">
                    <label for="description">Job DescriptionI </label>
                </div>
            </div>
            <div class="row">
                <input type="hidden" name="jobname" value="{{jobname}}">
                <button class="btn waves-effect waves-light" type="submit">Submit
                    <i class="material-icons right">send</i>
                </button>
            </div>
        </form>
    </div>

</div>