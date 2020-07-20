from dagster import (
    solid,
    pipeline,
    repository,
    ModeDefinition,
    default_executors,
)
from dagster_celery import celery_executor
from dagster.core.storage.pipeline_run import PipelineRunStatus, PipelineRunsFilter
from os import getenv
from requests import request
import time


celery_mode_defs = [ ModeDefinition(executor_defs=default_executors + [celery_executor]) ]


def start_bad_pipeline():

    query = r'''
        mutation {
          launchPipelineExecution(
            executionParams: {
              selector: {
                repositoryLocationName: "repository",
                repositoryName: "testing",
                pipelineName: "bad_pipeline",
              },
              mode: "default",
              runConfigData: {
                  execution: {
                      celery: {}
                  },
                  storage: {
                      filesystem: {}
                  },
              },
            }
          ) {
            ...launchPipelineExecutionResultFragment
          }
        }

        fragment launchPipelineExecutionResultFragment on LaunchPipelineExecutionResult {
          __typename
          ... on InvalidStepError {
            invalidStepKey
          }
          ... on InvalidOutputError {
            stepKey
            invalidOutputName
          }
          ... on LaunchPipelineRunSuccess {
            run {
              runId
              status
              pipeline {
                name
              }
              runConfigYaml
              mode
            }
          }
          ... on ConflictingExecutionParamsError {
            message
          }
          ... on PresetNotFoundError {
            preset
            message
          }
          ... on PipelineConfigValidationInvalid {
            pipelineName
            errors {
              __typename
              message
              path
              reason
            }
          }
          ... on PipelineNotFoundError {
            message
            pipelineName
          }
          ... on PythonError {
            message
            stack
          }
          ... on PipelineRunConflict {
            message
          }
        }
    '''

    return request(
        'post',
        f'http://{getenv("DAGSTER_HOST", "localhost")}:{getenv("DAGSTER_PORT", 9090)}/graphql',
        json=dict(query=query)
    ).json()


def wait_for_run_slot(context, pipeline_name, max_runs=1):

    def get_active_runs(pipeline_name):
        started_runs = len(context.instance.get_runs(PipelineRunsFilter(pipeline_name=pipeline_name, status=PipelineRunStatus.STARTED)))
        not_started_runs = len(context.instance.get_runs(PipelineRunsFilter(pipeline_name=pipeline_name, status=PipelineRunStatus.NOT_STARTED)))
        return started_runs + not_started_runs

    while get_active_runs(pipeline_name) >= max_runs:
        context.log.info(f"Found at least {max_runs} active runs for pipeline '{pipeline_name}', waiting.")
        time.sleep(2)

    context.log.info("Wait complete.")


@solid
def good_solid(context):
    context.log.info("Let's let 'wait_for_run_slot' run forever to demonstrate that it doesn't leak connections!")
    wait_for_run_slot(context, 'good_pipeline', 1)


@pipeline(mode_defs=celery_mode_defs)
def good_pipeline():
    good_solid()


@solid
def bad_pipeline_spawner(context):
    while True:
        wait_for_run_slot(context, 'bad_pipeline', 1)
        start_bad_pipeline()


@pipeline
def bad_pipeline_parent():
    bad_pipeline_spawner()


@solid
def sleeper(_):
    time.sleep(2)


@pipeline(mode_defs=celery_mode_defs)
def bad_pipeline():
    sleeper()


@repository
def testing():
    return [
        good_pipeline,
        bad_pipeline_parent,
        bad_pipeline,
    ]
