% rebase('base.tpl', title='CWD Overview', refreshinterval=60, scripturl='')
<div class="container">
    <div id="chart"></div>
    <div class="row">
        <div class="col s12 m12 l6">
            <div class="card-panel blue">
          <div class="card-title white-text">Currently Running Jobs</div>
              % for job in runjobs:
                <div class="black-text"><a class="white-text" href="{{ get_url('/jobs/<name>', name=job.name) }}">{{ job.name }}</a> - {{ str(job.eventtime)[0:19]}}</div>
              % end
            </div>
        </div>
        <div class="col s12 m12 l6">
            <div class="card-panel red">
            <div class="card-title white-text">Active Alarms</div>
              % for alarm in alarms:
                <div class="black-text"><a class="white-text" href="{{ get_url('/jobs/<name>', name=alarm.name) }}">{{ alarm.name }}</a> - {{ str(alarm.eventtime)[0:19]}}  {{ statuslookup[alarm.raisedevent] }}</div>
              % end
            </div>
            </div>
        </div>
    <h5 class="center-align">24 Hour Summary</h5>
    <div class="collection">
        <a href="#!" class="collection-item">Success<span class="badge white-text green">{{ summary['end'] }}</span></a>
        <a href="#!" class="collection-item">Failed<span
                class="badge white-text orange">{{ summary['fail'] }}</span></a>
        <a href="#!" class="collection-item">Alarms<span class="badge white-text red">{{ summary['alarm'] }}</span></a>
        <a href="#!" class="collection-item">Running<span class="badge white-text blue">{{ summary['current'] }}</span></a>
    </div>
    <div>
        <table class="responsive-table highlight bordered">
            <tr>
                <th>Job</th>
                <th>Event Time</th>
                <th>Run Time</th>
                <th>Status</th>
            </tr>
            % for job in lastjobs:
            <tr>
                <td><a href="{{ get_url('/jobs/<name>', name=job.name) }}">{{ job.name }}</a></td>
                <td>{{ str(job.eventtime)[1:19] }}</td>
                <td>{{ job.runtime }}</td>
                <td>
                    <div class="chip {{!"green" if job.status == 'end' else "red"}}">{{ statuslookup[job.status] }}</div>
    </td>
    </tr>
    % end
    </table>
  </div>
</div>
<script>
    var chart = c3.generate({
    title: {
        text: 'Job Counts'
    },
    data: {
        x: 'x',
        columns: [
            ['x',
            % for date in landingtrend:
                 '{{date}}',
            % end
            ],
            ['Complete Jobs',
                % for date in landingtrend:
                 {{ landingtrend[date]['end'] }},
                % end
            ],
            ['Failed Jobs',
                % for date in landingtrend:
                 {{ landingtrend[date]['fail'] }},
                % end
            ]
        ]
    },
    axis: {
        x: {
            type: 'timeseries',
            tick: {
                format: '%Y-%m-%d',
                rotate: 90
            }
        }
    },
    zoom: {
        enabled: true
    }
});


</script>