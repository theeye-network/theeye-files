import uvicorn, os
from fastapi import FastAPI, Depends, HTTPException, Header
from pydantic import BaseModel
from fastapi.responses import FileResponse
from typing import Dict
from modules import crud
from modules import auth
from modules import xlink
from modules import utils

app = FastAPI()

class UserCredentials(BaseModel):
	username: str
	password: str

@app.post("/log_in")
def log_in(credentials: UserCredentials):

	student = xlink.profiler(credentials.username,
					  credentials.password)

	if student.get("message")  == "valid":
		user_data = {"roll": credentials.username,
					 "name": student["student"][0][2],
					 "team": crud.getTeam(credentials.username)
					 }
		if crud.getTeam(credentials.username).get("message") == "invalid":
			return {"message": "404 Team Not Found"}
		jwt_token = auth.generate_jwt(user_data)
		return {"token": jwt_token, "message": "200 Success"}
	else:
		raise HTTPException(status_code=401, detail="Invalid credentials")

@app.get("/leaderboard")
def see_leaderboard():

	teams = crud.getTeams()

	for team in teams:
		team["flags"] = len(team["flags"])

	return crud.getTeams()


@app.get("/domains")
def see_domains(token:Dict = Depends(auth.verify_jwt)):

	domains = crud.getDomains()
	for domain in domains:
		domain["challenges"] = utils.maskFlags(domain["challenges"], token)

	return domains


@app.get("/challenges/{domain_name}")
def see_challenges(domain_name:str, token:Dict = Depends(auth.verify_jwt)):

	challenges = utils.maskFlags(crud.getDomain(domain_name)["challenges"], token)

	return challenges

@app.get("/challenges")
def see_challenges(token:Dict = Depends(auth.verify_jwt)):

	domains = crud.getDomains()
	challenges = utils.maskFlags(
					sorted(
						[challenge for domain in domains for challenge in domain["challenges"]],
						key=lambda challenge: len(challenge["flags"]),
						reverse=True),
					token)


	return challenges

@app.get("/challenge/{challenge_name}")
def see_challenge(challenge_name:str, token:Dict = Depends(auth.verify_jwt)):

	domains = crud.getDomains()
	challenges = utils.maskFlags(
					sorted([challenge for domain in domains for challenge in domain["challenges"]],
						key=lambda challenge: len(challenge["flags"]),
						reverse=True),
					token)

	return next((challenge for challenge in challenges if challenge["name"].lower()==challenge_name.lower()), {"message":"Not Found"})

@app.get("/challenge/{challenge_name}/files")
def get_files(challenge_name:str):
	domains = crud.getDomains()
	challenges = sorted([challenge for domain in domains for challenge in domain["challenges"]], key=lambda challenge: len(challenge["flags"]), reverse=True)

	challenge = next((challenge for challenge in challenges if challenge["name"].lower()==challenge_name.lower()), {"message":"Not Found"})

	file_path = os.path.join("static", f"{challenge['name']}_files.zip")
	
	if os.path.exists(file_path):
		return FileResponse(file_path, headers={"Content-Disposition": f"attachment; filename={challenge['name']}_files.zip"})
	else:
		return {"error": "File not found"}


@app.get("/search")
def get_files(q:str, token:Dict = Depends(auth.verify_jwt)):

	challenges = utils.maskFlags(crud.search_challenges(q),
								 token)

	return challenges

@app.post("/submit/{challenge_name}")
def submit_flag(challenge_name:str, submission:str, token:Dict = Depends(auth.verify_jwt)):

	domains = crud.getDomains()
	challenges = sorted([challenge for domain in domains for challenge in domain["challenges"]], key=lambda challenge: len(challenge["flags"]), reverse=True)

	challenge = next((challenge for challenge in challenges if challenge["name"].lower()==challenge_name.lower()), {"message":"Not Found"})

	for flag in challenge["flags"]:
		if submission == flag["id"]:
			return crud.addFlagToTeam(token.get("roll"),
									  flag,
									  challenge["name"])
	return {"message": "invalid"}

@app.get("/progress")
def getProgress(token:Dict = Depends(auth.verify_jwt)):

	return utils.generate_progress_report(token.get("roll"))


if __name__ == '__main__':
	uvicorn.run(app, host="0.0.0.0", port=5000)