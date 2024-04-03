import time
from prefect import flow, serve
from prefect import flow
from prefect.artifacts import create_link_artifact

@flow
def slow_flow(sleep: int = 60):
    "Sleepy flow - sleeps the provided amount of time (in seconds)."
    time.sleep(sleep)


@flow()
def fast_flow():
    "Fastest flow this side of the Mississippi."
    create_link_artifact(key="create-link-artifact", link="my_flow", description="## my_flow")
    return


if __name__ == "__main__":
    slow_deploy = slow_flow.to_deployment(name="sleeper", interval=45)
    fast_deploy = fast_flow.to_deployment(name="fast")
    serve(slow_deploy, fast_deploy)