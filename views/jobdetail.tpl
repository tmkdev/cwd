% rebase('base.tpl', title='CWD Job Status - {0}'.format(jobname), refreshinterval=60, scripturl='')
  <div class="container">
      <h5 class="center-align">Job Detail - {{jobname}}</h5>
      <div id="chart"></div>
       <table class="responsive-table highlight bordered">
              <tr>
                  <th>Job</th>
                  <th>Event Time</th>
                  <th>Run Time</th>
                  <th>Status</th>
              </tr>
              % for job in lastjobs:
                <tr>
                    <td>{{ job.name }}</td>
                    <td>{{ str(job.eventtime)[1:19] }}</td>
                    <td>{{ job.runtime }}</td>
                    <td>
                        <div class="chip {{!"green" if job.status == 'end' else "red"}}">{{ statuslookup[job.status] }}</div>
                    </td>
                </tr>
              % end
          </table>
  </div>

   <script>
    var chart = c3.generate({
    title: {
        text: 'Job Landing Times'
    },
    data: {
        x: 'x',
        xFormat: '%Y-%m-%d %H:%M:%S',
        columns: [
            ['x',
            % for log in landinglogs:
                 '{{ str(log.eventtime)[0:19] }}',
            % end
            ],
            ['Run Time',
                % for log in landinglogs:
                 {{ log.runtime }},
                % end
            ]
        ]
    },
    axis: {
        x: {
            type: 'timeseries',
            tick: {
                format: '%Y-%m-%d %H:%M',
                rotate: 90
            }
        }
    },
    zoom: {
        enabled: true
    }
});
</script>