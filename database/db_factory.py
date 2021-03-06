from typing import Union

from ipso_phen.ipapi.database.base import DbInfo, DbWrapper

from ipso_phen.ipapi.database.sqlite_wrapper import SqLiteDbWrapper
from ipso_phen.ipapi.database.psql_wrapper import PgSqlDbWrapper

try:
    from ipso_phen.ipapi.database.phenoserre_wrapper import PhenoserreDbWrapper
except Exception as e:
    is_phenoserre = False
else:
    is_phenoserre = True

try:
    from ipso_phen.ipapi.database.phenopsis_wrapper import PhenopsisDbWrapper
except Exception as e:
    is_phenopsis = False
else:
    is_phenopsis = True

try:
    from ipso_phen.ipapi.database.db_connect_data import db_connect_data as dbc
except Exception as e:
    dbc = {}


def db_info_to_database(info: DbInfo, **kwargs) -> Union[DbWrapper, str]:
    """Connects to a database from information, may create DB if needed and able

    Arguments:
        info {DbInfo} -- Describes the database

    Returns:
        [DbWrapper, str] -- Database wrapper if success, string descriging the problem else
    """
    if info.target == "psql_local":
        return PgSqlDbWrapper(
            **dbc.get(info.target, {}),
            db_info=info.copy(),
            progress_call_back=kwargs.get("progress_call_back", None),
        )
    elif info.target == "sqlite":
        return SqLiteDbWrapper(
            db_info=info.copy(),
            **dbc.get(info.target, {}),
            progress_call_back=kwargs.get("progress_call_back", None),
            db_folder_name=info.db_folder_name,
        )
    elif info.target == "phenoserre" and is_phenoserre is True:
        return PhenoserreDbWrapper(
            db_info=info.copy(),
            progress_call_back=kwargs.get("progress_call_back", None),
        )
    elif info.target == "phenopsis" and is_phenopsis is True:
        return PhenopsisDbWrapper(
            db_info=info.copy(),
            progress_call_back=kwargs.get("progress_call_back", None),
        )
    else:
        return f"Unknown target {info.target}"
