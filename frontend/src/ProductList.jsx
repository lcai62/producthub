import React, { useEffect, useState } from 'react';
import './App.css'; // or wherever you keep your styles

export default function ProductList() {

  const [products, setProducts] = useState([]);
  const [categories, setCategories] = useState([]);
  const [tags, setTags] = useState([]);

  const [selectedCategory, setSelectedCategory] = useState('');
  const [selectedTags, setSelectedTags] = useState([]);
  const [search, setSearch] = useState('');

  const [nextPage, setNextPage] = useState(null);
  const [prevPage, setPrevPage] = useState(null);

  useEffect(() => {
    fetch('http://localhost:8000/api/categories/')
      .then(res => res.json())
      .then(data => setCategories(data));

    fetch('http://localhost:8000/api/tags/')
      .then(res => res.json())
      .then(data => setTags(data));
  }, []);

  useEffect(() => {
    const params = new URLSearchParams();

    if (search) {
      params.append('description', search);
    }

    if (selectedCategory) {
      params.append('category', selectedCategory);
    }


    if (selectedTags.length > 0) {
      params.append('tags', selectedTags.join(','));
    }

    fetch(`http://localhost:8000/api/products/?${params.toString()}`)
      .then(res => res.json())
      .then(data => {
        setProducts(data.results || []);
        setNextPage(data.next);
        setPrevPage(data.previous);
      });
  }, [search, selectedCategory, selectedTags]);


  const loadPage = (url) => {
  fetch(url)
    .then(res => res.json())
    .then(data => {
      setProducts(data.results || []);
      setNextPage(data.next);
      setPrevPage(data.previous);
    });
};

  const toggleTag = (name) => {
    setSelectedTags(prev =>
      prev.includes(name) ? prev.filter(t => t !== name) : [...prev, name]
    );
  };

  return (
      <div className="container">
          <h1>Product Explorer</h1>

          <div className="search-bar">
              <input
                  type="text"
                  placeholder="Search by description..."
                  value={search}
                  onChange={(e) => setSearch(e.target.value)}
              />
          </div>

          <div className="filters">
              <div className="category">
                  <h3>Category</h3>
                  {categories.map(c => (
                      <label key={c.name}>
                          <input
                              type="radio"
                              name="category"
                              value={c.name}
                              checked={selectedCategory === c.name}
                              onClick={() =>
                                  setSelectedCategory(prev => prev === c.name ? '' : c.name)
                              }
                          />
                          {c.name}
                      </label>
                  ))}
              </div>

              <div className="tags">
                  <h3>Tags</h3>
                  {tags.map(t => (
                      <label key={t.name}>
                          <input
                              type="checkbox"
                              value={t.name}
                              checked={selectedTags.includes(t.name)}
                              onChange={() => toggleTag(t.name)}
                          />
                          {t.name}
                      </label>
                  ))}
              </div>
          </div>

          <div className="product-grid">
              {products.map(p => (
                  <div key={p.id} className="product-card">
                      <img
                          src={p.image}
                          alt={p.name}
                          onError={(e) => e.target.style.display = 'none'}
                      />
                      <h4>{p.name}</h4>
                      <p className="description">{p.description}</p>
                      <div className="meta">
                          <span className="category">{p.category.name}</span>
                          <span className="price">${p.price}</span>
                      </div>
                      <div className="tags">
                          {p.tags.map(tag => (
                              <span key={tag.name} className="tag">{tag.name}</span>
                          ))}
                      </div>
                  </div>
              ))}
          </div>

          <div className="pagination">
              {prevPage && <button onClick={() => loadPage(prevPage)}>⬅ Prev</button>}
              {nextPage && <button onClick={() => loadPage(nextPage)}>Next ➡</button>}
          </div>

      </div>
  );
}
