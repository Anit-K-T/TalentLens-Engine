def recommend(score):

    if score >= 90:
        return "⭐⭐⭐⭐⭐ Highly Recommended"

    elif score >= 70:
        return "⭐⭐⭐⭐ Recommended"

    elif score >= 50:
        return "⭐⭐⭐ Consider"

    else:
        return "⭐⭐ Not Recommended"