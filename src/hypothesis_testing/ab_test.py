"""
A/B Testing Framework
Author: Gabriel Demetrios Lafis
Description: Statistical framework for A/B testing with frequentist and Bayesian approaches
"""

import numpy as np
from scipy import stats
from typing import Dict


class ABTest:
    """
    A comprehensive A/B testing framework for conversion rate optimization.
    """

    def __init__(self, alpha: float = 0.05, power: float = 0.80):
        """
        Initialize the A/B test framework.

        Parameters:
        -----------
        alpha : float
            Significance level (Type I error rate)
        power : float
            Statistical power (1 - Type II error rate)
        """
        self.alpha = alpha
        self.power = power
        self.beta = 1 - power

    def calculate_sample_size(self, baseline_rate: float, mde: float, ratio: float = 1.0) -> int:
        """
        Calculate required sample size for an A/B test.

        Parameters:
        -----------
        baseline_rate : float
            Current conversion rate (between 0 and 1)
        mde : float
            Minimum detectable effect (relative change, e.g., 0.1 for 10%)
        ratio : float
            Ratio of treatment to control group size

        Returns:
        --------
        int : Required sample size per group
        """
        if not (0 < baseline_rate < 1):
            raise ValueError("baseline_rate must be between 0 and 1 (exclusive)")
        if mde <= 0:
            raise ValueError("mde must be greater than 0")
        if ratio <= 0:
            raise ValueError("ratio must be greater than 0")

        p1 = baseline_rate
        p2 = baseline_rate * (1 + mde)

        if p2 >= 1:
            raise ValueError(
                f"Resulting treatment rate ({p2:.4f}) must be less than 1. "
                "Reduce baseline_rate or mde."
            )

        # Pooled proportion
        p_pooled = (p1 + ratio * p2) / (1 + ratio)

        # Z-scores
        z_alpha = stats.norm.ppf(1 - self.alpha / 2)
        z_beta = stats.norm.ppf(self.power)

        # Sample size calculation
        numerator = (
            z_alpha * np.sqrt(p_pooled * (1 - p_pooled) * (1 + 1 / ratio))
            + z_beta * np.sqrt(p1 * (1 - p1) + p2 * (1 - p2) / ratio)
        ) ** 2
        denominator = (p2 - p1) ** 2

        n = int(np.ceil(numerator / denominator))

        return n

    def two_proportion_ztest(
        self, conversions_a: int, visitors_a: int, conversions_b: int, visitors_b: int
    ) -> Dict:
        """
        Perform a two-proportion z-test for A/B testing.

        Parameters:
        -----------
        conversions_a : int
            Number of conversions in group A (control)
        visitors_a : int
            Number of visitors in group A
        conversions_b : int
            Number of conversions in group B (treatment)
        visitors_b : int
            Number of visitors in group B

        Returns:
        --------
        dict : Test results including p-value, confidence interval, and effect size
        """
        if visitors_a <= 0 or visitors_b <= 0:
            raise ValueError("Number of visitors must be greater than 0")
        if conversions_a < 0 or conversions_b < 0:
            raise ValueError("Number of conversions cannot be negative")
        if conversions_a > visitors_a or conversions_b > visitors_b:
            raise ValueError("Conversions cannot exceed visitors")

        # Handle edge case where both groups have zero conversions
        if conversions_a == 0 and conversions_b == 0:
            return {
                "conversion_rate_a": 0.0,
                "conversion_rate_b": 0.0,
                "absolute_difference": 0.0,
                "relative_lift": 0.0,
                "z_statistic": 0.0,
                "p_value": 1.0,
                "is_significant": False,
                "confidence_interval": (0.0, 0.0),
                "confidence_level": 1 - self.alpha,
            }

        # Calculate proportions
        p_a = conversions_a / visitors_a
        p_b = conversions_b / visitors_b

        # Pooled proportion
        p_pooled = (conversions_a + conversions_b) / (visitors_a + visitors_b)

        # Standard error
        se = np.sqrt(p_pooled * (1 - p_pooled) * (1 / visitors_a + 1 / visitors_b))

        # Z-statistic
        z_stat = (p_b - p_a) / se

        # P-value (two-tailed)
        p_value = 2 * (1 - stats.norm.cdf(abs(z_stat)))

        # Confidence interval for the difference
        z_critical = stats.norm.ppf(1 - self.alpha / 2)
        se_diff = np.sqrt(p_a * (1 - p_a) / visitors_a + p_b * (1 - p_b) / visitors_b)
        ci_lower = (p_b - p_a) - z_critical * se_diff
        ci_upper = (p_b - p_a) + z_critical * se_diff

        # Relative lift
        relative_lift = (p_b - p_a) / p_a if p_a > 0 else 0

        results = {
            "conversion_rate_a": p_a,
            "conversion_rate_b": p_b,
            "absolute_difference": p_b - p_a,
            "relative_lift": relative_lift,
            "z_statistic": z_stat,
            "p_value": p_value,
            "is_significant": p_value < self.alpha,
            "confidence_interval": (ci_lower, ci_upper),
            "confidence_level": 1 - self.alpha,
        }

        return results

    def bayesian_ab_test(
        self,
        conversions_a: int,
        visitors_a: int,
        conversions_b: int,
        visitors_b: int,
        n_simulations: int = 100000,
    ) -> Dict:
        """
        Perform Bayesian A/B test using Beta distributions.

        Parameters:
        -----------
        conversions_a : int
            Number of conversions in group A
        visitors_a : int
            Number of visitors in group A
        conversions_b : int
            Number of conversions in group B
        visitors_b : int
            Number of visitors in group B
        n_simulations : int
            Number of Monte Carlo simulations

        Returns:
        --------
        dict : Bayesian test results
        """
        if visitors_a <= 0 or visitors_b <= 0:
            raise ValueError("Number of visitors must be greater than 0")
        if conversions_a < 0 or conversions_b < 0:
            raise ValueError("Number of conversions cannot be negative")
        if conversions_a > visitors_a or conversions_b > visitors_b:
            raise ValueError("Conversions cannot exceed visitors")

        # Prior: Beta(1, 1) - uniform prior
        alpha_prior = 1
        beta_prior = 1

        # Posterior distributions
        alpha_a = alpha_prior + conversions_a
        beta_a = beta_prior + (visitors_a - conversions_a)

        alpha_b = alpha_prior + conversions_b
        beta_b = beta_prior + (visitors_b - conversions_b)

        # Sample from posterior distributions
        rng = np.random.default_rng()
        samples_a = rng.beta(alpha_a, beta_a, n_simulations)
        samples_b = rng.beta(alpha_b, beta_b, n_simulations)

        # Probability that B is better than A
        prob_b_better = np.mean(samples_b > samples_a)

        # Expected loss
        expected_loss_b = np.mean(np.maximum(samples_a - samples_b, 0))
        expected_loss_a = np.mean(np.maximum(samples_b - samples_a, 0))

        # Credible intervals
        ci_a = np.percentile(samples_a, [2.5, 97.5])
        ci_b = np.percentile(samples_b, [2.5, 97.5])

        results = {
            "prob_b_better_than_a": prob_b_better,
            "prob_a_better_than_b": 1 - prob_b_better,
            "expected_loss_choosing_b": expected_loss_b,
            "expected_loss_choosing_a": expected_loss_a,
            "credible_interval_a": ci_a,
            "credible_interval_b": ci_b,
            "posterior_mean_a": np.mean(samples_a),
            "posterior_mean_b": np.mean(samples_b),
        }

        return results

    def print_results(self, results: Dict, test_type: str = "frequentist"):
        """
        Print formatted test results.
        """
        print("=" * 60)
        print(f"A/B TEST RESULTS ({test_type.upper()})")
        print("=" * 60)

        if test_type == "frequentist":
            print(f"Conversion Rate A: {results['conversion_rate_a']:.4f}")
            print(f"Conversion Rate B: {results['conversion_rate_b']:.4f}")
            print(f"Absolute Difference: {results['absolute_difference']:.4f}")
            print(f"Relative Lift: {results['relative_lift']:.2%}")
            print(f"Z-Statistic: {results['z_statistic']:.4f}")
            print(f"P-Value: {results['p_value']:.4f}")
            print(f"Significant: {results['is_significant']}")
            confidence_pct = results.get('confidence_level', 1 - self.alpha) * 100
            print(
                f"{confidence_pct:.0f}% CI: ({results['confidence_interval'][0]:.4f}, {results['confidence_interval'][1]:.4f})"
            )

        elif test_type == "bayesian":
            print(f"Probability B > A: {results['prob_b_better_than_a']:.2%}")
            print(f"Probability A > B: {results['prob_a_better_than_b']:.2%}")
            print(f"Expected Loss (choosing B): {results['expected_loss_choosing_b']:.6f}")
            print(f"Expected Loss (choosing A): {results['expected_loss_choosing_a']:.6f}")
            print(f"Posterior Mean A: {results['posterior_mean_a']:.4f}")
            print(f"Posterior Mean B: {results['posterior_mean_b']:.4f}")

        print("=" * 60)


# Example usage
if __name__ == "__main__":
    # Initialize the framework
    ab_test = ABTest(alpha=0.05, power=0.80)

    # Calculate required sample size
    print("Sample Size Calculation:")
    print("-" * 60)
    sample_size = ab_test.calculate_sample_size(
        baseline_rate=0.10, mde=0.20  # 20% relative improvement
    )
    print(f"Required sample size per group: {sample_size}")
    print()

    # Example data
    conversions_a = 120
    visitors_a = 1500
    conversions_b = 145
    visitors_b = 1500

    # Frequentist test
    freq_results = ab_test.two_proportion_ztest(
        conversions_a, visitors_a, conversions_b, visitors_b
    )
    ab_test.print_results(freq_results, "frequentist")
    print()

    # Bayesian test
    bayes_results = ab_test.bayesian_ab_test(conversions_a, visitors_a, conversions_b, visitors_b)
    ab_test.print_results(bayes_results, "bayesian")
