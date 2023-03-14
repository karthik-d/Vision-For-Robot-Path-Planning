function true_realdistance = shortest_distance(poin1, poin2, obstacl1)

    % Calculate the difference between the two points in each dimension
    pqx = poin2(1,1) - poin1(1,1);
	pqy = poin2(1,2) - poin1(1,2);
	pqz = poin2(1,3) - poin1(1,3);
	dx = obstacl1(1,1) - poin1(1,1);
	dy = obstacl1(1,2) - poin1(1,2);
	dz = obstacl1(1,3) - poin1(1,3);

    % Calculate the squared distance between the two points
	d_1 = pqx*pqx + pqy*pqy + pqz*pqz;

    % Calculate the projection of the obstacle point onto the line between the two given points
	t_2 = pqx*dx + pqy*dy + pqz*dz;

    % Calculate the value of t, which represents the relative position of the projection along the line
	t_1 = t_2 / d_1;

    % If t is less than 0, the projection falls outside the line segment and we take the distance to the first point
	if (t_1 < 0)
		t_1 = 0;
    % If t is greater than 1, the projection falls outside the line segment and we take the distance to the second point
	else if (t_1 > 1)
		t_1 = 1;
    % If t is between 0 and 1, the projection falls inside the line segment and we take the distance to the line
        else
            t_1 = 2;
        end
    end
    
    % Calculate the distance to the obstacle based on the value of t
    if t_1 == 0
        true_realdistance = Distance(poin1,obstacl1);
    end
    if t_1 == 1
         true_realdistance = Distance(poin2,obstacl1);
    end
    if t_1 == 2
         true_realdistance = point_to_line(poin1,poin2,obstacl1);
    end

end

function realdistance = point_to_line(point1, point2, obstacle1)

    % Calculate the vector between the two given points
    vx1x2 = point2 - point1;

    % Calculate the vector between the first point and the obstacle
    vx1x3 = obstacle1 - point1;

    % Calculate the inner product of the two vectors
    inner_product = dot(vx1x2, vx1x3);

    % Calculate the square of the inner product
    inner_product_2 = inner_product * inner_product;

    % Calculate the square of the cosine of the angle between the two vectors
    cos_2 = inner_product_2 / dot(vx1x2,vx1x2) / dot(vx1x3, vx1x3);

    % Calculate the square of the sine of the angle between the two vectors
    sin_2 = 1 - cos_2;

    % Calculate the square of the distance between the first point and the line connecting the two points
    dis_2 = dot(vx1x3,vx1x3) * sin_2;

    % Calculate the distance between the obstacle and the line connecting the two points
    realdistance = sqrt(dis_2);

end

function dist = Distance(X, Y)
    % Calculate Chebyshev distance
    dist_chebyshev = max(abs(X-Y));
    
    % Calculate Manhattan distance and count the number of non-aligned coordinates
    non_aligned = find(X ~= Y);
    dist_manhattan = sum(abs(X(non_aligned) - Y(non_aligned)));
    num_non_aligned = length(non_aligned);
    
    % Calculate Minkowski distance
    if num_non_aligned == 0
        dist_minkowski = dist_chebyshev;
    else
        dist_minkowski = (dist_manhattan / num_non_aligned) ^ (num_non_aligned / (num_non_aligned - 1));
    end
    
    % Return the maximum of Chebyshev and Minkowski distances
    dist = max(dist_chebyshev, dist_minkowski);
end
