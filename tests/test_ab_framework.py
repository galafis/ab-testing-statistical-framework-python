"""
Comprehensive test suite for A/B Testing Framework
Author: Gabriel Demetrios Lafis
"""

import pytest
import numpy as np
from src.hypothesis_testing.ab_test import ABTest


class TestABTestInitialization:
    """Test ABTest class initialization"""

    def test_default_initialization(self):
        """Test default alpha and power values"""
        ab_test = ABTest()
        assert ab_test.alpha == 0.05
        assert ab_test.power == 0.80
        assert ab_test.beta == pytest.approx(0.20)

    def test_custom_initialization(self):
        """Test custom alpha and power values"""
        ab_test = ABTest(alpha=0.01, power=0.90)
        assert ab_test.alpha == 0.01
        assert ab_test.power == 0.90
        assert ab_test.beta == pytest.approx(0.10)


class TestSampleSizeCalculation:
    """Test sample size calculation functionality"""

    def test_sample_size_calculation_baseline(self):
        """Test sample size calculation with typical values"""
        ab_test = ABTest(alpha=0.05, power=0.80)
        sample_size = ab_test.calculate_sample_size(baseline_rate=0.10, mde=0.20)
        # Expected sample size should be around 3841
        assert isinstance(sample_size, int)
        assert sample_size > 0
        assert 3800 <= sample_size <= 3900

    def test_sample_size_increases_with_smaller_mde(self):
        """Test that smaller MDE requires larger sample size"""
        ab_test = ABTest(alpha=0.05, power=0.80)

        sample_size_large_mde = ab_test.calculate_sample_size(baseline_rate=0.10, mde=0.30)

        sample_size_small_mde = ab_test.calculate_sample_size(baseline_rate=0.10, mde=0.10)

        assert sample_size_small_mde > sample_size_large_mde

    def test_sample_size_with_different_ratios(self):
        """Test sample size calculation with different group ratios"""
        ab_test = ABTest(alpha=0.05, power=0.80)

        sample_size_1_1 = ab_test.calculate_sample_size(baseline_rate=0.10, mde=0.20, ratio=1.0)

        sample_size_2_1 = ab_test.calculate_sample_size(baseline_rate=0.10, mde=0.20, ratio=2.0)

        assert isinstance(sample_size_1_1, int)
        assert isinstance(sample_size_2_1, int)
        assert sample_size_1_1 > 0
        assert sample_size_2_1 > 0

    def test_sample_size_with_higher_power(self):
        """Test that higher power requires larger sample size"""
        ab_test_80 = ABTest(alpha=0.05, power=0.80)
        ab_test_90 = ABTest(alpha=0.05, power=0.90)

        sample_size_80 = ab_test_80.calculate_sample_size(baseline_rate=0.10, mde=0.20)

        sample_size_90 = ab_test_90.calculate_sample_size(baseline_rate=0.10, mde=0.20)

        assert sample_size_90 > sample_size_80


class TestTwoProportionZTest:
    """Test two-proportion z-test functionality"""

    def test_z_test_with_known_data(self):
        """Test z-test with example data from documentation"""
        ab_test = ABTest(alpha=0.05, power=0.80)

        results = ab_test.two_proportion_ztest(
            conversions_a=120, visitors_a=1500, conversions_b=145, visitors_b=1500
        )

        # Verify result structure
        assert "conversion_rate_a" in results
        assert "conversion_rate_b" in results
        assert "absolute_difference" in results
        assert "relative_lift" in results
        assert "z_statistic" in results
        assert "p_value" in results
        assert "is_significant" in results
        assert "confidence_interval" in results
        assert "confidence_level" in results

        # Verify conversion rates
        assert results["conversion_rate_a"] == pytest.approx(0.08, abs=0.001)
        assert results["conversion_rate_b"] == pytest.approx(0.0967, abs=0.001)

        # Verify absolute difference
        assert results["absolute_difference"] > 0

        # Verify relative lift
        assert results["relative_lift"] > 0

        # Verify confidence interval is a tuple of length 2
        assert isinstance(results["confidence_interval"], tuple)
        assert len(results["confidence_interval"]) == 2

        # Verify confidence level
        assert results["confidence_level"] == 0.95

    def test_z_test_significant_difference(self):
        """Test z-test with statistically significant difference"""
        ab_test = ABTest(alpha=0.05, power=0.80)

        # Large difference should be significant
        results = ab_test.two_proportion_ztest(
            conversions_a=100, visitors_a=1000, conversions_b=200, visitors_b=1000
        )

        assert results["is_significant"] == True
        assert results["p_value"] < 0.05

    def test_z_test_no_difference(self):
        """Test z-test with no difference between groups"""
        ab_test = ABTest(alpha=0.05, power=0.80)

        results = ab_test.two_proportion_ztest(
            conversions_a=100, visitors_a=1000, conversions_b=100, visitors_b=1000
        )

        assert results["conversion_rate_a"] == results["conversion_rate_b"]
        assert results["absolute_difference"] == pytest.approx(0, abs=1e-10)
        assert results["relative_lift"] == pytest.approx(0, abs=1e-10)
        assert results["is_significant"] == False
        assert results["p_value"] > 0.05

    def test_z_test_confidence_interval_contains_difference(self):
        """Test that confidence interval contains the true difference"""
        ab_test = ABTest(alpha=0.05, power=0.80)

        results = ab_test.two_proportion_ztest(
            conversions_a=120, visitors_a=1500, conversions_b=145, visitors_b=1500
        )

        ci_lower, ci_upper = results["confidence_interval"]

        # For non-significant results, CI should contain zero
        # For significant results, CI should not contain zero
        if results["is_significant"]:
            assert not (ci_lower < 0 < ci_upper)
        else:
            assert ci_lower < 0 < ci_upper or abs(ci_lower) < 0.001 or abs(ci_upper) < 0.001

    def test_z_test_relative_lift_calculation(self):
        """Test relative lift calculation"""
        ab_test = ABTest(alpha=0.05, power=0.80)

        results = ab_test.two_proportion_ztest(
            conversions_a=100, visitors_a=1000, conversions_b=120, visitors_b=1000
        )

        # Manual calculation
        rate_a = 100 / 1000
        rate_b = 120 / 1000
        expected_lift = (rate_b - rate_a) / rate_a

        assert results["relative_lift"] == pytest.approx(expected_lift, abs=1e-10)

    def test_z_test_with_zero_baseline(self):
        """Test z-test behavior with zero conversions in control"""
        ab_test = ABTest(alpha=0.05, power=0.80)

        results = ab_test.two_proportion_ztest(
            conversions_a=0, visitors_a=1000, conversions_b=10, visitors_b=1000
        )

        # Should handle zero baseline gracefully
        assert results["conversion_rate_a"] == 0
        assert results["conversion_rate_b"] > 0
        assert results["relative_lift"] == 0  # As per code logic


class TestBayesianABTest:
    """Test Bayesian A/B test functionality"""

    def test_bayesian_test_basic(self):
        """Test basic Bayesian test functionality"""
        ab_test = ABTest(alpha=0.05, power=0.80)

        results = ab_test.bayesian_ab_test(
            conversions_a=120,
            visitors_a=1500,
            conversions_b=145,
            visitors_b=1500,
            n_simulations=10000,
        )

        # Verify result structure
        assert "prob_b_better_than_a" in results
        assert "prob_a_better_than_b" in results
        assert "expected_loss_choosing_b" in results
        assert "expected_loss_choosing_a" in results
        assert "credible_interval_a" in results
        assert "credible_interval_b" in results
        assert "posterior_mean_a" in results
        assert "posterior_mean_b" in results

        # Probabilities should sum to approximately 1
        assert results["prob_b_better_than_a"] + results["prob_a_better_than_b"] == pytest.approx(
            1.0, abs=1e-10
        )

        # Probabilities should be between 0 and 1
        assert 0 <= results["prob_b_better_than_a"] <= 1
        assert 0 <= results["prob_a_better_than_b"] <= 1

        # Expected losses should be non-negative
        assert results["expected_loss_choosing_b"] >= 0
        assert results["expected_loss_choosing_a"] >= 0

        # Credible intervals should be arrays of length 2
        assert len(results["credible_interval_a"]) == 2
        assert len(results["credible_interval_b"]) == 2

        # Lower bound should be less than upper bound
        assert results["credible_interval_a"][0] < results["credible_interval_a"][1]
        assert results["credible_interval_b"][0] < results["credible_interval_b"][1]

    def test_bayesian_test_clear_winner(self):
        """Test Bayesian test with clear winner"""
        ab_test = ABTest(alpha=0.05, power=0.80)

        results = ab_test.bayesian_ab_test(
            conversions_a=100,
            visitors_a=1000,
            conversions_b=200,
            visitors_b=1000,
            n_simulations=10000,
        )

        # B should clearly be better than A
        assert results["prob_b_better_than_a"] > 0.95
        assert results["expected_loss_choosing_b"] < results["expected_loss_choosing_a"]

    def test_bayesian_test_equal_groups(self):
        """Test Bayesian test with equal performance"""
        ab_test = ABTest(alpha=0.05, power=0.80)

        results = ab_test.bayesian_ab_test(
            conversions_a=100,
            visitors_a=1000,
            conversions_b=100,
            visitors_b=1000,
            n_simulations=10000,
        )

        # Probabilities should be approximately equal
        assert 0.4 < results["prob_b_better_than_a"] < 0.6
        assert 0.4 < results["prob_a_better_than_b"] < 0.6

    def test_bayesian_test_posterior_means(self):
        """Test that posterior means are reasonable"""
        ab_test = ABTest(alpha=0.05, power=0.80)

        results = ab_test.bayesian_ab_test(
            conversions_a=120,
            visitors_a=1500,
            conversions_b=145,
            visitors_b=1500,
            n_simulations=10000,
        )

        # Posterior means should be close to observed rates
        observed_rate_a = 120 / 1500
        observed_rate_b = 145 / 1500

        assert results["posterior_mean_a"] == pytest.approx(observed_rate_a, abs=0.01)
        assert results["posterior_mean_b"] == pytest.approx(observed_rate_b, abs=0.01)

    def test_bayesian_test_monte_carlo_stability(self):
        """Test that results are reasonably stable across runs (Monte Carlo variation)"""
        ab_test = ABTest(alpha=0.05, power=0.80)

        results1 = ab_test.bayesian_ab_test(
            conversions_a=120,
            visitors_a=1500,
            conversions_b=145,
            visitors_b=1500,
            n_simulations=100000,
        )

        results2 = ab_test.bayesian_ab_test(
            conversions_a=120,
            visitors_a=1500,
            conversions_b=145,
            visitors_b=1500,
            n_simulations=100000,
        )

        # With 100k simulations, results should be stable within ~1%
        assert results1["prob_b_better_than_a"] == pytest.approx(
            results2["prob_b_better_than_a"], abs=0.02
        )


class TestPrintResults:
    """Test result printing functionality"""

    def test_print_frequentist_results(self, capsys):
        """Test printing frequentist results"""
        ab_test = ABTest(alpha=0.05, power=0.80)

        results = ab_test.two_proportion_ztest(
            conversions_a=120, visitors_a=1500, conversions_b=145, visitors_b=1500
        )

        ab_test.print_results(results, "frequentist")

        captured = capsys.readouterr()
        assert "A/B TEST RESULTS (FREQUENTIST)" in captured.out
        assert "Conversion Rate A:" in captured.out
        assert "Conversion Rate B:" in captured.out
        assert "P-Value:" in captured.out
        assert "Significant:" in captured.out

    def test_print_bayesian_results(self, capsys):
        """Test printing Bayesian results"""
        ab_test = ABTest(alpha=0.05, power=0.80)

        results = ab_test.bayesian_ab_test(
            conversions_a=120,
            visitors_a=1500,
            conversions_b=145,
            visitors_b=1500,
            n_simulations=10000,
        )

        ab_test.print_results(results, "bayesian")

        captured = capsys.readouterr()
        assert "A/B TEST RESULTS (BAYESIAN)" in captured.out
        assert "Probability B > A:" in captured.out
        assert "Expected Loss" in captured.out


class TestEdgeCases:
    """Test edge cases and error conditions"""

    def test_very_small_sample_sizes(self):
        """Test behavior with very small sample sizes"""
        ab_test = ABTest(alpha=0.05, power=0.80)

        results = ab_test.two_proportion_ztest(
            conversions_a=1, visitors_a=10, conversions_b=2, visitors_b=10
        )

        assert isinstance(results, dict)
        assert "p_value" in results

    def test_all_conversions(self):
        """Test with 100% conversion rate"""
        ab_test = ABTest(alpha=0.05, power=0.80)

        results = ab_test.two_proportion_ztest(
            conversions_a=100, visitors_a=100, conversions_b=100, visitors_b=100
        )

        assert results["conversion_rate_a"] == 1.0
        assert results["conversion_rate_b"] == 1.0
        assert results["absolute_difference"] == 0.0

    def test_high_baseline_rate(self):
        """Test sample size calculation with high baseline rate"""
        ab_test = ABTest(alpha=0.05, power=0.80)

        sample_size = ab_test.calculate_sample_size(baseline_rate=0.90, mde=0.05)

        assert isinstance(sample_size, int)
        assert sample_size > 0

    def test_very_low_baseline_rate(self):
        """Test sample size calculation with very low baseline rate"""
        ab_test = ABTest(alpha=0.05, power=0.80)

        sample_size = ab_test.calculate_sample_size(baseline_rate=0.01, mde=0.50)

        assert isinstance(sample_size, int)
        assert sample_size > 0


class TestIntegration:
    """Integration tests for complete workflows"""

    def test_complete_ab_test_workflow(self):
        """Test a complete A/B test workflow"""
        # Initialize framework
        ab_test = ABTest(alpha=0.05, power=0.80)

        # Step 1: Calculate required sample size
        sample_size = ab_test.calculate_sample_size(baseline_rate=0.10, mde=0.20)
        assert sample_size > 0

        # Step 2: Run frequentist test
        freq_results = ab_test.two_proportion_ztest(
            conversions_a=120, visitors_a=1500, conversions_b=145, visitors_b=1500
        )
        assert "p_value" in freq_results

        # Step 3: Run Bayesian test
        bayes_results = ab_test.bayesian_ab_test(
            conversions_a=120,
            visitors_a=1500,
            conversions_b=145,
            visitors_b=1500,
            n_simulations=10000,
        )
        assert "prob_b_better_than_a" in bayes_results

        # Both tests should provide insights
        assert freq_results["is_significant"] in [True, False]
        assert 0 <= bayes_results["prob_b_better_than_a"] <= 1

    def test_different_alpha_levels(self):
        """Test framework with different significance levels"""
        for alpha in [0.01, 0.05, 0.10]:
            ab_test = ABTest(alpha=alpha, power=0.80)

            results = ab_test.two_proportion_ztest(
                conversions_a=120, visitors_a=1500, conversions_b=145, visitors_b=1500
            )

            assert results["confidence_level"] == 1 - alpha
