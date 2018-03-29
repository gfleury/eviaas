from flask import request

from evi import app, db
from model import Plan, Env, Instance
import json

@app.route("/resources/plans", methods=["GET"])
def get_plans():
    plans = Plan.query.all()
    return json.dumps(Plan.serialize_list(plans)), 200

# {"name": "salve", "description": "salve"}
@app.route("/resources/plans", methods=["POST"])
def put_plans():
    content = request.get_json(silent=True)
    plan = Plan(content)
    db.session.add(plan)
    db.session.commit()
    return "Plan created", 200

# {"key": "salve", "value": "salve"}
@app.route("/resources/plans/<planname>/env", methods=["POST"])
def put_env(planname):
    plan = Plan.query.filter_by(name=planname).first()
    content = request.get_json(silent=True)
    env = Env(content)
    env.plan = plan
    db.session.add(env)
    db.session.commit()
    return "Env on plan created", 200

@app.route("/resources/plans/<planname>/envs", methods=["GET"])
def get_envs(planname):
    plan = Plan.query.filter_by(name=planname).first()
    envs = Env.query.filter_by(plan=plan)
    return json.dumps(Env.serialize_list(envs)), 200

@app.route("/resources", methods=["POST"])
def add_instance():
    plan = Plan.query.filter_by(name=request.form.get('plan')).first()
    data = request.form.copy()
    instance = Instance(data)
    instance.plan = plan
    db.session.add(instance)
    db.session.commit()
    return "", 201

@app.route("/resources/<name>", methods=["GET"])
def get_instance(name):
    instance = Instance.query.filter_by(name=name).first()
    return json.dumps(instance.serialize()), 200

@app.route("/resources/<name>", methods=["PUT"])
def update_instance(name):
    return "", 200


@app.route("/resources/<name>", methods=["DELETE"])
def remove_instance(name):
    instance = Instance.query.filter_by(name=name).first()
    db.session.delete(instance)
    db.session.commit()
    return "", 200


@app.route("/resources/<name>/bind", methods=["DELETE"])
@app.route("/resources/<name>/bind-app", methods=["DELETE"])
def unbind(name):
    return "", 200


@app.route("/resources/<name>/bind", methods=["POST"])
@app.route("/resources/<name>/bind-app", methods=["POST"])
def bind(name):
    instance = Instance.query.filter_by(name=name).first()
    envs = Env.query.filter_by(plan=instance.plan)
    return json.dumps(Env.serialize_json(envs)), 201


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8888, debug=True)
