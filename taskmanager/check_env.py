from decouple import config

print("EMAIL_HOST_USER:", config('EMAIL_HOST_USER'))
print("EMAIL_HOST_PASSWORD:", config('EMAIL_HOST_PASSWORD'))