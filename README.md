# dagster-testing

To reproduce the issue, open 4 terminal windows on the project root and run each of these commands in a different terminal:

```
make run6
```

```
make monitor6
```

```
make run7
```

```
make monitor7
```

Then open 2 browser tabs, one for [0.8.6](http://localhost:9091/pipeline/bad_pipeline_parent/playground) and one for [0.8.7](http://localhost:9092/pipeline/bad_pipeline_parent/playground).

Launch the `bad_pipeline_parent` pipeline in both 0.8.6 and 0.8.7. Switch to the monitor6 and monitor7 tabs and watch how in 0.8.6 the postgres connection count is normal, while in 0.8.7 there is a connection leak. About 10 mins after launch, the 0.8.7 pipeline's `bad_pipeline` children will start erroring out with a Postgres "too many clients" error, while 0.8.6 continues to work fine indefinitely.

This issue is easy to spot in pgAdmin:
<img src="pgadmin.png" />
X axis spans about 2 mins.

0.8.8 inherits this bug from 0.8.7, as can be confirmed from running `make run8` and `make monitor8`.
