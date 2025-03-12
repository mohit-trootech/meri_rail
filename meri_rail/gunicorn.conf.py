def post_fork(server, worker):
    from utils.selenium_service import SeleniumService

    SeleniumService()


bind = "0.0.0.0:8000"
workers = 1
