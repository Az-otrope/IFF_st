import streamlit as st


def homepage():
    st.title("Sparkle Too Data Analysis")

    st.write(
        """
            This web application is a data analysis and management platform for Sparkle Too portfolio.

            Users can navigate to pages from the left sidebar:

                * Master Sample Registration
                * In-pack
                * On-seed
                * Boost

            Each project page allows users to perform various actions to interact with the database such as input sample's information, upload experimental data, and
            retreive reports for further analysis.

            Start exploring and using this platform by selecting a project for detailed instructions.

            Have fun and keep experimenting!

                """
    )

    st.info("Contact Nguyen at nguyen.pham@iff for feedback and questions")
    st.snow()
