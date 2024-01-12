def get_ssm_parameter(ssm, parameter_name, with_decryption=False):
    return ssm.get_parameter(Name=parameter_name, WithDecryption=with_decryption)[
        "Parameter"
    ]["Value"]
