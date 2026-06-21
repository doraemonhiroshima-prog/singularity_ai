# core/investment/capital_allocator.py

class CapitalAllocator:

    # =====================================================
    # ALLOCATE
    # =====================================================
    def allocate(
        self,
        cash,
        signals
    ):

        result = []

        try:

            if len(signals) == 0:

                return result

            # =========================
            # SCORE TOTAL
            # =========================
            total_score = 0

            for s in signals:

                total_score += max(
                    s.get("score", 1),
                    1
                )

            if total_score <= 0:

                return result

            # =========================
            # ALLOCATE
            # =========================
            for s in signals:

                score = max(
                    s.get("score", 1),
                    1
                )

                ratio = (
                    score / total_score
                )

                capital = cash * ratio

                s["capital"] = capital

                result.append(s)

            return result

        except:

            return []