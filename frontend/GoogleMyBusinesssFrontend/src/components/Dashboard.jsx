import React, { useEffect, useState } from 'react';
import axios from 'axios';
import './Dashboard.css';

function Dashboard() {
  const [reviews, setReviews] = useState([]);
  const [newReview, setNewReview] = useState({
    photo_url: '',
    name: '',
    date: '',
    stars: '',
    content: '',
  });
  const [reply, setReply] = useState('');
  const [selectedReviewId, setSelectedReviewId] = useState(null);

  // Fetch reviews from the backend
  useEffect(() => {
    axios
      .get('http://localhost:8000/reviews/')
      .then((response) => {
        setReviews(response.data);
      })
      .catch((error) => {
        console.error('Error fetching reviews:', error);
      });
  }, []);

  // Handle new review submission
  const handleNewReviewSubmit = (e) => {
    e.preventDefault();
    axios
      .post('http://localhost:8000/reviews/', newReview)
      .then((response) => {
        setReviews([...reviews, response.data]); // Add new review to the list
        setNewReview({
          photo_url: '',
          name: '',
          date: '',
          stars: '',
          content: '',
        });
      })
      .catch((error) => {
        console.error('Error adding review:', error);
      });
  };

  // Handle reply submission
  const handleReplySubmit = (reviewId) => {
    axios
      .post(`http://localhost:8000/reviews/${reviewId}/reply/`, { reply_content: reply })
      .then((response) => {
        const updatedReviews = reviews.map((review) =>
          review.id === reviewId ? { ...review, replies: [...review.replies, response.data] } : review
        );
        setReviews(updatedReviews); // Update reviews with new reply
        setReply(''); // Clear reply input
      })
      .catch((error) => {
        console.error('Error adding reply:', error);
      });
  };

  return (
    <div className="dashboard">
      <h1>Customer Reviews</h1>
      
      {/* Display reviews */}
      {reviews.map((review) => (
        <div key={review.id} className="review">
          <img src={review.photo_url} alt="Reviewer" width="100" />
          <h3>{review.name}</h3>
          <p>{review.date}</p>
          <p>Rating: {review.stars}</p>
          <p>{review.content}</p>
          
          <h4>Replies</h4>
          {review.replies && review.replies.length > 0 ? (
            <ul>
              {review.replies.map((reply, replyIndex) => (
                <li key={replyIndex}>{reply.reply_content}</li>
              ))}
            </ul>
          ) : (
            <p>No replies yet</p>
          )}

          {/* Input to submit a reply */}
          <input
            type="text"
            placeholder="Write a reply..."
            value={selectedReviewId === review.id ? reply : ''}
            onChange={(e) => {
              setSelectedReviewId(review.id);
              setReply(e.target.value);
            }}
          />
          <button onClick={() => handleReplySubmit(review.id)}>Reply</button>
        </div>
      ))}

      {/* Add new review */}
      <h2>Add New Review</h2>
      <form onSubmit={handleNewReviewSubmit}>
        <input
          type="text"
          placeholder="Photo URL"
          value={newReview.photo_url}
          onChange={(e) => setNewReview({ ...newReview, photo_url: e.target.value })}
        />
        <input
          type="text"
          placeholder="Name"
          value={newReview.name}
          onChange={(e) => setNewReview({ ...newReview, name: e.target.value })}
        />
       <input
  type="date"
  value={newReview.date}
  onChange={(e) => setNewReview({ ...newReview, date: e.target.value })}
/>

        <input
          type="number"
          placeholder="Stars (1-5)"
          value={newReview.stars}
          onChange={(e) => setNewReview({ ...newReview, stars: e.target.value })}
          min="1"
          max="5"
        />
        <textarea
          placeholder="Review content"
          value={newReview.content}
          onChange={(e) => setNewReview({ ...newReview, content: e.target.value })}
        />
        <button type="submit">Submit Review</button>
      </form>
    </div>
  );
}

export default Dashboard;
