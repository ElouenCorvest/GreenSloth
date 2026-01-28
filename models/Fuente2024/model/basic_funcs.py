def mass_action_1s(s1: float, k_fwd: float) -> float:
    return k_fwd * s1

def moiety_1(concentration: float, total: float) -> float:
    return total - concentration

