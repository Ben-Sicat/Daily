pub mod math;

impl math{
    pub fn distance_between_ponints(p1: &na::Point3<64>, p2: &na::Point3<64>) -> f64 {
        // Calculate the Euclidean distance between two 3D points
        let dx = p1.x - p2.x;
        let dy = p1.y - p2.y;
        let dz = p1.z - p2.z;
        (dx * dx + dy * dy + dz * dz).sqrt()
    }
}

#[cfg(test)]
mod test{
    use super::*;
    fn test_distance_between_points(){
        let p1 = na::Point3::new(1.0, 2.0, 3.0);
        let p2 = na::Point3::new(4.0, 5.0, 6.0);
        let distance = math::distance_between_points(&p1, &p2);
        assert_eq!(distance, 5.196152422706632);
    }
}