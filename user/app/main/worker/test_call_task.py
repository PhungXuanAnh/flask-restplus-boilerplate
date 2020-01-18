from app.main.worker.tasks import crawl

# crawl.apply_async(('facebook', 'Cristiano', 1531019563, 1567579502, 'localhost'), countdown=3)
crawl.apply_async(('facebook', 'Cristiano', 1531019563, 1567579502), countdown=3)
