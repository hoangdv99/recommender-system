import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from scipy import sparse

class CF(object):
    def __init__(self, Y_data, k, dist_func = cosine_similarity, uuCF = 1):
    #Y_data: ma tran Utility
    #k: so luong cac diem lan can de du doan ket qua
    #dist_func: ham do similarity giua 2 vector
    #uuCF: 1: user-user   0: item-item
        self.uuCF = uuCF
        self.Y_data = Y_data if uuCF else Y_data[:, [1, 0, 2]]
        self.k = k
        self.dist_func = dist_func
        self.Ybar_data = None
        self.n_users = int(np.max(self.Y_data[:, 0])) + 1
        self.n_items = int(np.max(self.Y_data[:, 1])) + 1
    
    #Update Y_data matrix when new ratings come.
    def add(self, new_data):
        self.Y_data = np.concatenate((self.Y_data, new_data), axis = 0)
        print(self.Y_data)
    
    def normalize_Y(self):
        users = self.Y_data[:, 0] # all users - first col of the Y_data
        self.Ybar_data = self.Y_data.copy()
        self.mu = np.zeros((self.n_users,))
        for n in range(self.n_users):
            # row indices of rating done by user n
            # since indices need to be integers, we need to convert
            ids = np.where(users == n)[0].astype(np.int32)
            item_ids = self.Y_data[ids, 1]   # indices of all ratings associated with user n
            ratings = self.Y_data[ids, 2]    # and the corresponding ratings 
            m = np.mean(ratings)             # take mean
            if np.isnan(m):
                m = 0                        # to avoid empty array and nan value
            self.mu[n] = m
            self.Ybar_data[ids, 2] = ratings - self.mu[n]   # normalize

        ################################################
        # form the rating matrix as a sparse matrix. Sparsity is important 
        # for both memory and computing efficiency. For example, if #user = 1M, 
        # #item = 100k, then shape of the rating matrix would be (100k, 1M), 
        # you may not have enough memory to store this. Then, instead, we store 
        # nonzeros only, and, of course, their locations.
        self.Ybar = sparse.coo_matrix((self.Ybar_data[:, 2],
            (self.Ybar_data[:, 1], self.Ybar_data[:, 0])), (self.n_items, self.n_users))
        self.Ybar = self.Ybar.tocsr()

    def similarity(self):
        self.S = self.dist_func(self.Ybar.T, self.Ybar.T)
    
    def refresh(self):
        self.normalize_Y()
        self.similarity()
    
    def fit(self):
        self.refresh()

    def __pred(self, u, i, normalized = 1):
        #find all users rated i
        ids = np.where(self.Y_data[:, 1] == i)[0].astype(np.int32)
        users_rated_i = (self.Y_data[ids, 0]).astype(np.int32)
        # Step 3: find similarity btw the current user and others 
        # who already rated i
        sim = self.S[u, users_rated_i]
        a = np.argsort(sim)[-self.k:]     # Step 4: find the k most similarity users
        nearest_s = sim[a]                # and the corresponding similarity levels
        r = self.Ybar[i, users_rated_i[a]]   # How did each of 'near' users rated item i
        if normalized:
            return (r*nearest_s)[0]/(np.abs(nearest_s).sum() + 1e-8)   # add a small number, for instance, 1e-8, to avoid dividing by 0
        return (r*nearest_s)[0]/(np.abs(nearest_s).sum() + 1e-8) + self.mu[u]

    def pred(self, u, i, normalized = 1):
        """ 
        predict the rating of user u for item i (normalized)
        if you need the un
        """
        if self.uuCF: return self.__pred(u, i, normalized)
        return self.__pred(i, u, normalized)

    def recommend(self, u):
        """
        Determine all items should be recommended for user u.
        The decision is made based on all i such that:
        self.pred(u, i) > 0. Suppose we are considering items which 
        have not been rated by u yet. 
        """
        ids = np.where(self.Y_data[:, 0] == u)[0]
        print(ids)
        items_rated_by_u = self.Y_data[ids, 1].tolist()              
        recommended_items = []
        for i in range(self.n_items):
            if i not in items_rated_by_u:
                rating = self.__pred(u, i)
                if rating > 0: 
                    recommended_items.append(i)
        
        return recommended_items
    
    def print_recommendation(self):
        print('Recommendation: ')
        for u in range(self.n_users):
            recommended_items = self.recommend(u)
            if self.uuCF:
                print('Recommend item(s):', recommended_items, 'for user', u)
            else: 
                print('Recommend item', u, 'for user(s) : ', recommended_items)

