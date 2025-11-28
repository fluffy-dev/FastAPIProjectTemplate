
### endpoints:
#### auth part (public):
- /login
- /registration

#### user (not protected):
- POST: / - create user
- GET: /{pk} - get user
- DELETE: /{pk} - delete user
- PATCH: /{pk} - update user

### login flow:
1. get user login data from LoginDTO - interface/router layer
2. router: LoginDTO -> auth service
3. auth service: LoginDTO -> TokenService decode
4. TokenService 