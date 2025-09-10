import numpy as np


def price_reverse_convertible_multi(S0, barriers, r, sigmas, corr, T, N_paths, dt=1 / 252, principal=100.0,
                                    coupon_rate=0.1, compute_delta=False, bump=0.01):
    """
    The code comes from Grok ... it took him 3 seconds...
    Price a multi-barrier (multi-asset) reverse convertible using Monte Carlo.
    Optionally compute delta using finite differences with common random numbers.

    Parameters:
    - S0: array of initial prices (e.g., [100, 100, 100, 100] for 4 assets)
    - barriers: array of down barriers (e.g., [70, 70, 70, 70])
    - r: risk-free rate (e.g., 0.05)
    - sigmas: array of volatilities (e.g., [0.2, 0.25, 0.18, 0.22])
    - corr: correlation matrix (e.g., 4x4 matrix)
    - T: time to maturity in years
    - N_paths: number of Monte Carlo paths
    - dt: time step (small for barrier accuracy)
    - principal: nominal value
    - coupon_rate: annual coupon rate
    - compute_delta: if True, return price and deltas (vector for each asset)
    - bump: relative bump for finite difference (e.g., 0.01 for 1%)

    Returns: price if compute_delta=False, else (price, deltas)
    """
    n_assets = len(S0)
    print(n_assets)
    corr_matrix = np.array(corr)
    L = np.linalg.cholesky(corr_matrix)  # For correlated normals

    n_steps = int(T / dt)

    # Generate randoms once for common numbers
    np.random.seed(42)  # For reproducibility
    Z = np.random.normal(0, 1, (n_steps, n_assets, N_paths))  # Pre-generate all Z

    def simulate_paths(S0_base):
        paths = np.zeros((n_steps + 1, n_assets, N_paths))
        paths[0] = np.tile(S0_base[:, np.newaxis], (1, N_paths))

        sigmas_arr = sigmas[:, np.newaxis]  # Reshape

        for t in range(1, n_steps + 1):
            dz = np.dot(L, Z[t - 1]) * np.sqrt(dt)
            drift = (r - 0.5 * sigmas_arr ** 2) * dt
            paths[t] = paths[t - 1] * np.exp(drift + sigmas_arr * dz)

        return paths

    def compute_payoffs(paths, S0_base):
        min_paths = np.min(paths[1:], axis=0)
        hit = np.any(min_paths < barriers[:, np.newaxis], axis=0)

        ST = paths[-1]

        payoffs = np.zeros(N_paths)
        total_coupons = principal * coupon_rate * T
        for i in range(N_paths):
            if not hit[i]:
                payoffs[i] = principal + total_coupons
            else:
                worst_perf = np.min(ST[:, i] / S0_base)
                payoffs[i] = principal * worst_perf
        return payoffs

    # Base case
    paths_base = simulate_paths(S0)
    payoffs_base = compute_payoffs(paths_base, S0)
    price = np.mean(payoffs_base) * np.exp(-r * T)

    if not compute_delta:
        return price

    # Compute delta for each asset
    deltas = np.zeros(n_assets)
    for j in range(n_assets):
        dS = bump * S0[j]

        # Up bump
        S0_up = S0.copy()
        S0_up[j] += dS
        paths_up = simulate_paths(S0_up)
        payoffs_up = compute_payoffs(paths_up, S0_up)
        price_up = np.mean(payoffs_up) * np.exp(-r * T)

        # Down bump
        S0_down = S0.copy()
        S0_down[j] -= dS
        paths_down = simulate_paths(S0_down)
        payoffs_down = compute_payoffs(paths_down, S0_down)
        price_down = np.mean(payoffs_down) * np.exp(-r * T)

        deltas[j] = (price_up - price_down) / (2 * dS)

    return price, deltas