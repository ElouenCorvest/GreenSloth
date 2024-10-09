# Define the newest version of the model
from modelbase.ode import Model

from pathlib import Path
import sys

sys.path.append(str(Path(__file__).parent))

from module_atp_synthase import add_ATPase
from module_consistency_check import add_consistency_check
from module_consuming_reactions import add_consuming_reactions
from module_electron_transport_chain import add_electron_transport_chain
from module_photorespiratory_salvage import add_photorespiratory_salvage
from module_rubisco_reactions import add_CBB_and_oxy
from module_update_FlvandCCM import update_CCM, update_Flv_hill
from module_update_statetransitions import update_statetransitions_hill
from module_update_CBB import update_CBBactivation_hill, update_CBBactivation_MM
from module_update_phycobilisomes import add_OCP
from module_update_NQ import update_NQ_MM

import parameters


def get_model(
    get_y0=True,
    check_consistency=True,
    pbs_behaviour="static",
    reduced_size=False,
    verbose=True,
    init_param=None,
):
    m = Model()
    m = add_electron_transport_chain(
        m,
        init_param=init_param,
        pbs_behaviour=pbs_behaviour,
        reduced_size=reduced_size,
        verbose=verbose,
    )
    m = add_ATPase(m, init_param=init_param)
    m = add_consuming_reactions(m, init_param=init_param)
    m = add_CBB_and_oxy(m, init_param=init_param)
    m = add_photorespiratory_salvage(m, init_param=init_param)

    # Set initial values
    # Adapt according to PBS behaviour and potentially initial parameters
    y0 = parameters.y0.copy()
    if pbs_behaviour == "dynamic":
        y0.update(
            {k: v for k, v in parameters.p.items() if k in ["PBS_PS1", "PBS_PS2"]}
        )
        if init_param is not None:
            y0.update(
                {k: v for k, v in init_param.items() if k in ["PBS_PS1", "PBS_PS2"]}
            )

    # Add the newest updates
    m, y0 = update_statetransitions_hill(m, y0, init_param=init_param, verbose=verbose)
    m, y0 = update_Flv_hill(m, y0, init_param=init_param, verbose=verbose)
    m, y0 = update_CCM(m, y0, init_param=init_param, verbose=verbose)
    # m, y0 = update_CBBactivation_hill(m, y0, verbose=verbose)
    m, y0 = update_CBBactivation_MM(m, y0, verbose=verbose)    
    m, y0 = add_OCP(m, y0, verbose=verbose)
    m, y0 = update_NQ_MM(m, y0, verbose=verbose)

    ## TRANSIENT CHANGES
    # None at the moment

    if check_consistency:
        m = add_consistency_check(m)
        print(
            "Consistency checks added, this might slow the model down.\nIf the model works fine, set check_consistency=False"
        )

    if get_y0:
        # Return the model and initial conditions
        return m, y0
    else:
        return m
