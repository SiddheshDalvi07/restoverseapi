import { createSlice } from "@reduxjs/toolkit";

const authSlice = createSlice({
    name: "auth",
    initialState: {
        user: null,
        accessToken: null,
        reviews: [],      // Store reviews in the state
    },
    reducers: {
        setAuthUser: (state, action) => {
            state.user = action.payload;
        },
        setToken: (state, action) => {
            state.accessToken = action.payload;
        },
        setReviews: (state, action) => {
            state.reviews = action.payload;  // Set all reviews
        },
        addReview: (state, action) => {
            state.reviews.push(action.payload);  // Add new review
        },
        addReply: (state, action) => {
            const { reviewId, reply } = action.payload;
            const review = state.reviews.find(r => r._id === reviewId);  // Find the review by ID
            if (review) {
                review.replies.push(reply);  // Add reply to the review
            }
        },
    }
});

export const {
    setAuthUser,
    setToken,
    setReviews,
    addReview,
    addReply,
} = authSlice.actions;

export default authSlice.reducer;
