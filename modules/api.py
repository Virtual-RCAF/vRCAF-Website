if __name__ == "__main__":
    raise TypeError(f"'{__file__}' is a module and should be imported not executed directly")


from os import environ
from aiomysql import connect, OperationalError
from utils.responses import ResponseMessageDict
from flask import Blueprint, request


api = Blueprint("api", __name__)


@api.route("/api/v1/roster/<cid>")
async def user_by_cid(cid: int):
    cid = int(cid)
    if not isinstance(cid, int):
        parse = ResponseMessageDict.RESP_URLARG
        parse["message"] = parse["message"].format(
            "CID",
            "int",
            str(type(cid))
        )
        return parse, 400
    else:
        auth = request.headers.get("vRCAF-CA")
        if auth is None:
            return ResponseMessageDict.RESP_NOTAUTH, 401
        try:
            async with connect(
                user=environ.get("DATABASE_USER"),
                password=environ.get("DATABASE_PASS"),
                db="vrcaf"
            ) as db:
                cursor = await db.cursor()
                await cursor.execute(
                    "SELECT * FROM dev_users WHERE cid = %s",
                    (
                        cid
                    )
                )
                results = await cursor.fetchall()
                if len(results) == 0:
                    return ResponseMessageDict.RESP_USRNTF, 404
                else:
                    return {
                        "message": "Operation successful",
                        "data": results[0]
                    }, 200
        except OperationalError:
            return ResponseMessageDict.RESP_SRVERR, 500


def setup():
    return api
